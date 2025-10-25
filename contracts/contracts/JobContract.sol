// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title JobContract
 * @notice Stores cryptographic commitments for resume evaluations for a single job
 * @dev Each job posting gets its own contract instance deployed by JobFactory
 */
contract JobContract {
    // ═══════════════════════════════════════════════════════════════════════
    // STATE VARIABLES
    // ═══════════════════════════════════════════════════════════════════════
    
    /// @notice Address of the job owner (recruiter/company)
    address public jobOwner;
    
    /// @notice Hash of job configuration (job_id, requirements, etc.)
    bytes32 public jobConfigHash;
    
    /// @notice Job owner's public encryption key for encrypted communications
    bytes public jobOwnerPubEncKey;
    
    /// @notice Timestamp when the job was created
    uint256 public createdAt;
    
    /// @notice Factory contract that deployed this job
    address public factory;
    
    // ═══════════════════════════════════════════════════════════════════════
    // DATA STRUCTURES
    // ═══════════════════════════════════════════════════════════════════════
    
    /**
     * @notice Evaluation commitment structure
     * @dev Stores all cryptographic commitments for a single resume evaluation
     */
    struct EvaluationCommitment {
        bytes32 resumeHash;        // sha256 of anonymized resume text
        bytes32 modelHash;         // sha256 of ML model identifier
        bytes32 scoreHash;         // sha256 of canonical JSON score payload
        bytes32 encEmailHash;      // hash of encrypted applicant email (optional)
        uint256 timestamp;         // when the evaluation was committed
        bool exists;               // whether this commitment exists
    }
    
    /// @notice Mapping from submission_id to evaluation commitment
    mapping(bytes32 => EvaluationCommitment) public evaluations;
    
    /// @notice Array of all submission IDs for enumeration
    bytes32[] public submissionIds;
    
    // ═══════════════════════════════════════════════════════════════════════
    // EVENTS
    // ═══════════════════════════════════════════════════════════════════════
    
    /**
     * @notice Emitted when a new evaluation commitment is stored
     * @param submissionId Unique identifier for the submission
     * @param resumeHash Hash of the anonymized resume
     * @param scoreHash Hash of the evaluation score/decision
     * @param timestamp When the commitment was created
     */
    event EvaluationCommitted(
        bytes32 indexed submissionId,
        bytes32 resumeHash,
        bytes32 scoreHash,
        uint256 timestamp
    );
    
    // ═══════════════════════════════════════════════════════════════════════
    // MODIFIERS
    // ═══════════════════════════════════════════════════════════════════════
    
    /// @notice Only the job owner can call this function
    modifier onlyJobOwner() {
        require(msg.sender == jobOwner, "Only job owner");
        _;
    }
    
    /// @notice Only the factory contract can call this function
    modifier onlyFactory() {
        require(msg.sender == factory, "Only factory");
        _;
    }
    
    // ═══════════════════════════════════════════════════════════════════════
    // CONSTRUCTOR
    // ═══════════════════════════════════════════════════════════════════════
    
    /**
     * @notice Initialize a new job contract
     * @param _jobOwner Address of the job owner
     * @param _jobConfigHash Hash of job configuration
     * @param _jobOwnerPubEncKey Public encryption key of job owner
     */
    constructor(
        address _jobOwner,
        bytes32 _jobConfigHash,
        bytes memory _jobOwnerPubEncKey
    ) {
        require(_jobOwner != address(0), "Invalid job owner");
        require(_jobConfigHash != bytes32(0), "Invalid config hash");
        
        jobOwner = _jobOwner;
        jobConfigHash = _jobConfigHash;
        jobOwnerPubEncKey = _jobOwnerPubEncKey;
        createdAt = block.timestamp;
        factory = msg.sender;
    }
    
    // ═══════════════════════════════════════════════════════════════════════
    // CORE FUNCTIONS
    // ═══════════════════════════════════════════════════════════════════════
    
    /**
     * @notice Compute submission ID from applicant wallet, job ID, and resume hash
     * @dev This should match the backend calculation: keccak256(wallet_address || job_id || resume_hash)
     * @param walletAddress Applicant's Ethereum address
     * @param jobId Job identifier (can be same as jobConfigHash or separate)
     * @param resumeHash Hash of the anonymized resume
     * @return submissionId The computed submission identifier
     */
    function computeSubmissionId(
        address walletAddress,
        bytes32 jobId,
        bytes32 resumeHash
    ) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(walletAddress, jobId, resumeHash));
    }
    
    /**
     * @notice Store evaluation commitment on-chain
     * @dev Called by backend after ML service processes resume
     * @param submissionId Unique identifier for this submission
     * @param resumeHash sha256 of anonymized resume text
     * @param modelHash sha256 of ML model identifier
     * @param scoreHash sha256 of canonical JSON score payload
     * @param encEmailHash Hash of encrypted applicant email (can be zero)
     */
    function commitEvaluation(
        bytes32 submissionId,
        bytes32 resumeHash,
        bytes32 modelHash,
        bytes32 scoreHash,
        bytes32 encEmailHash
    ) external onlyJobOwner {
        require(submissionId != bytes32(0), "Invalid submission ID");
        require(resumeHash != bytes32(0), "Invalid resume hash");
        require(modelHash != bytes32(0), "Invalid model hash");
        require(scoreHash != bytes32(0), "Invalid score hash");
        require(!evaluations[submissionId].exists, "Evaluation already exists");
        
        evaluations[submissionId] = EvaluationCommitment({
            resumeHash: resumeHash,
            modelHash: modelHash,
            scoreHash: scoreHash,
            encEmailHash: encEmailHash,
            timestamp: block.timestamp,
            exists: true
        });
        
        submissionIds.push(submissionId);
        
        emit EvaluationCommitted(submissionId, resumeHash, scoreHash, block.timestamp);
    }
    
    /**
     * @notice Verify that an evaluation commitment matches expected values
     * @dev Used by applicants to verify their results haven't been tampered with
     * @param submissionId The submission to verify
     * @param resumeHash Expected resume hash
     * @param modelHash Expected model hash
     * @param scoreHash Expected score hash
     * @return isValid Whether all hashes match
     */
    function verifyEvaluation(
        bytes32 submissionId,
        bytes32 resumeHash,
        bytes32 modelHash,
        bytes32 scoreHash
    ) external view returns (bool) {
        EvaluationCommitment memory eval = evaluations[submissionId];
        
        if (!eval.exists) {
            return false;
        }
        
        return (
            eval.resumeHash == resumeHash &&
            eval.modelHash == modelHash &&
            eval.scoreHash == scoreHash
        );
    }
    
    /**
     * @notice Get evaluation commitment details
     * @param submissionId The submission to query
     * @return resumeHash Hash of anonymized resume
     * @return modelHash Hash of ML model
     * @return scoreHash Hash of evaluation score
     * @return encEmailHash Hash of encrypted email
     * @return timestamp When commitment was created
     * @return exists Whether commitment exists
     */
    function getEvaluation(bytes32 submissionId)
        external
        view
        returns (
            bytes32 resumeHash,
            bytes32 modelHash,
            bytes32 scoreHash,
            bytes32 encEmailHash,
            uint256 timestamp,
            bool exists
        )
    {
        EvaluationCommitment memory eval = evaluations[submissionId];
        return (
            eval.resumeHash,
            eval.modelHash,
            eval.scoreHash,
            eval.encEmailHash,
            eval.timestamp,
            eval.exists
        );
    }
    
    /**
     * @notice Get total number of submissions for this job
     * @return count Number of evaluation commitments
     */
    function getSubmissionCount() external view returns (uint256) {
        return submissionIds.length;
    }
    
    /**
     * @notice Get submission ID at a specific index
     * @param index Array index
     * @return submissionId The submission ID at that index
     */
    function getSubmissionIdAt(uint256 index) external view returns (bytes32) {
        require(index < submissionIds.length, "Index out of bounds");
        return submissionIds[index];
    }
}
