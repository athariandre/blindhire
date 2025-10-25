const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("BlindHire Contracts", function () {
  let jobFactory;
  let jobContract;
  let owner;
  let recruiter;
  let applicant;

  beforeEach(async function () {
    // Get signers
    [owner, recruiter, applicant] = await ethers.getSigners();

    // Deploy JobFactory
    const JobFactory = await ethers.getContractFactory("JobFactory");
    jobFactory = await JobFactory.deploy();
    await jobFactory.waitForDeployment();
  });

  describe("JobFactory", function () {
    it("Should deploy with correct platform owner", async function () {
      expect(await jobFactory.platformOwner()).to.equal(owner.address);
    });

    it("Should create a new job", async function () {
      const jobConfigHash = ethers.keccak256(ethers.toUtf8Bytes("job-123"));
      const pubKey = ethers.toUtf8Bytes("recruiter-pubkey");

      const tx = await jobFactory.connect(recruiter).createJob(jobConfigHash, pubKey);
      const receipt = await tx.wait();

      // Check event
      const event = receipt.logs.find(
        (log) => log.fragment && log.fragment.name === "JobCreated"
      );
      expect(event).to.not.be.undefined;

      // Get job address
      const jobAddress = await jobFactory.jobByConfigHash(jobConfigHash);
      expect(jobAddress).to.not.equal(ethers.ZeroAddress);

      // Verify job count
      expect(await jobFactory.getTotalJobs()).to.equal(1);
      expect(await jobFactory.getJobCountByOwner(recruiter.address)).to.equal(1);
    });

    it("Should not allow duplicate job config hash", async function () {
      const jobConfigHash = ethers.keccak256(ethers.toUtf8Bytes("job-123"));
      const pubKey = ethers.toUtf8Bytes("recruiter-pubkey");

      await jobFactory.connect(recruiter).createJob(jobConfigHash, pubKey);

      await expect(
        jobFactory.connect(recruiter).createJob(jobConfigHash, pubKey)
      ).to.be.revertedWith("Job already exists");
    });

    it("Should retrieve jobs by owner", async function () {
      const jobConfigHash1 = ethers.keccak256(ethers.toUtf8Bytes("job-1"));
      const jobConfigHash2 = ethers.keccak256(ethers.toUtf8Bytes("job-2"));
      const pubKey = ethers.toUtf8Bytes("recruiter-pubkey");

      await jobFactory.connect(recruiter).createJob(jobConfigHash1, pubKey);
      await jobFactory.connect(recruiter).createJob(jobConfigHash2, pubKey);

      const jobs = await jobFactory.getJobsByOwner(recruiter.address);
      expect(jobs.length).to.equal(2);
    });
  });

  describe("JobContract", function () {
    beforeEach(async function () {
      // Create a job
      const jobConfigHash = ethers.keccak256(ethers.toUtf8Bytes("job-123"));
      const pubKey = ethers.toUtf8Bytes("recruiter-pubkey");

      await jobFactory.connect(recruiter).createJob(jobConfigHash, pubKey);

      const jobAddress = await jobFactory.jobByConfigHash(jobConfigHash);
      jobContract = await ethers.getContractAt("JobContract", jobAddress);
    });

    it("Should have correct job owner", async function () {
      expect(await jobContract.jobOwner()).to.equal(recruiter.address);
    });

    it("Should compute submission ID correctly", async function () {
      const walletAddress = applicant.address;
      const jobId = ethers.keccak256(ethers.toUtf8Bytes("job-123"));
      const resumeHash = ethers.keccak256(ethers.toUtf8Bytes("resume-content"));

      const submissionId = await jobContract.computeSubmissionId(
        walletAddress,
        jobId,
        resumeHash
      );

      // Verify it matches keccak256(abi.encodePacked(...))
      const expected = ethers.keccak256(
        ethers.solidityPacked(
          ["address", "bytes32", "bytes32"],
          [walletAddress, jobId, resumeHash]
        )
      );
      expect(submissionId).to.equal(expected);
    });

    it("Should commit evaluation successfully", async function () {
      const submissionId = ethers.keccak256(ethers.toUtf8Bytes("submission-1"));
      const resumeHash = ethers.keccak256(ethers.toUtf8Bytes("resume-content"));
      const modelHash = ethers.keccak256(ethers.toUtf8Bytes("model-v1"));
      const scoreHash = ethers.keccak256(ethers.toUtf8Bytes('{"score": 0.85}'));
      const encEmailHash = ethers.keccak256(ethers.toUtf8Bytes("encrypted-email"));

      const tx = await jobContract
        .connect(recruiter)
        .commitEvaluation(
          submissionId,
          resumeHash,
          modelHash,
          scoreHash,
          encEmailHash
        );

      const receipt = await tx.wait();

      // Check event
      const event = receipt.logs.find(
        (log) => log.fragment && log.fragment.name === "EvaluationCommitted"
      );
      expect(event).to.not.be.undefined;

      // Verify evaluation was stored
      const evaluation = await jobContract.getEvaluation(submissionId);
      expect(evaluation.resumeHash).to.equal(resumeHash);
      expect(evaluation.modelHash).to.equal(modelHash);
      expect(evaluation.scoreHash).to.equal(scoreHash);
      expect(evaluation.encEmailHash).to.equal(encEmailHash);
      expect(evaluation.exists).to.be.true;
    });

    it("Should only allow job owner to commit evaluation", async function () {
      const submissionId = ethers.keccak256(ethers.toUtf8Bytes("submission-1"));
      const resumeHash = ethers.keccak256(ethers.toUtf8Bytes("resume-content"));
      const modelHash = ethers.keccak256(ethers.toUtf8Bytes("model-v1"));
      const scoreHash = ethers.keccak256(ethers.toUtf8Bytes('{"score": 0.85}'));
      const encEmailHash = ethers.ZeroHash;

      await expect(
        jobContract
          .connect(applicant)
          .commitEvaluation(
            submissionId,
            resumeHash,
            modelHash,
            scoreHash,
            encEmailHash
          )
      ).to.be.revertedWith("Only job owner");
    });

    it("Should not allow duplicate submission commitments", async function () {
      const submissionId = ethers.keccak256(ethers.toUtf8Bytes("submission-1"));
      const resumeHash = ethers.keccak256(ethers.toUtf8Bytes("resume-content"));
      const modelHash = ethers.keccak256(ethers.toUtf8Bytes("model-v1"));
      const scoreHash = ethers.keccak256(ethers.toUtf8Bytes('{"score": 0.85}'));
      const encEmailHash = ethers.ZeroHash;

      await jobContract
        .connect(recruiter)
        .commitEvaluation(
          submissionId,
          resumeHash,
          modelHash,
          scoreHash,
          encEmailHash
        );

      await expect(
        jobContract
          .connect(recruiter)
          .commitEvaluation(
            submissionId,
            resumeHash,
            modelHash,
            scoreHash,
            encEmailHash
          )
      ).to.be.revertedWith("Evaluation already exists");
    });

    it("Should verify evaluation correctly", async function () {
      const submissionId = ethers.keccak256(ethers.toUtf8Bytes("submission-1"));
      const resumeHash = ethers.keccak256(ethers.toUtf8Bytes("resume-content"));
      const modelHash = ethers.keccak256(ethers.toUtf8Bytes("model-v1"));
      const scoreHash = ethers.keccak256(ethers.toUtf8Bytes('{"score": 0.85}'));
      const encEmailHash = ethers.ZeroHash;

      await jobContract
        .connect(recruiter)
        .commitEvaluation(
          submissionId,
          resumeHash,
          modelHash,
          scoreHash,
          encEmailHash
        );

      // Verify with correct hashes
      expect(
        await jobContract.verifyEvaluation(
          submissionId,
          resumeHash,
          modelHash,
          scoreHash
        )
      ).to.be.true;

      // Verify with incorrect hash
      const wrongHash = ethers.keccak256(ethers.toUtf8Bytes("wrong"));
      expect(
        await jobContract.verifyEvaluation(
          submissionId,
          wrongHash,
          modelHash,
          scoreHash
        )
      ).to.be.false;
    });

    it("Should track submission count correctly", async function () {
      expect(await jobContract.getSubmissionCount()).to.equal(0);

      const submissionId1 = ethers.keccak256(ethers.toUtf8Bytes("submission-1"));
      const submissionId2 = ethers.keccak256(ethers.toUtf8Bytes("submission-2"));
      const resumeHash = ethers.keccak256(ethers.toUtf8Bytes("resume-content"));
      const modelHash = ethers.keccak256(ethers.toUtf8Bytes("model-v1"));
      const scoreHash = ethers.keccak256(ethers.toUtf8Bytes('{"score": 0.85}'));
      const encEmailHash = ethers.ZeroHash;

      await jobContract
        .connect(recruiter)
        .commitEvaluation(
          submissionId1,
          resumeHash,
          modelHash,
          scoreHash,
          encEmailHash
        );

      expect(await jobContract.getSubmissionCount()).to.equal(1);

      await jobContract
        .connect(recruiter)
        .commitEvaluation(
          submissionId2,
          resumeHash,
          modelHash,
          scoreHash,
          encEmailHash
        );

      expect(await jobContract.getSubmissionCount()).to.equal(2);
    });
  });
});
