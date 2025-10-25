// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./JobContract.sol";

/**
 * @title JobFactory
 * @notice Factory contract for deploying JobContract instances
 * @dev Manages job creation and tracks all deployed job contracts
 */
contract JobFactory {
    // ═══════════════════════════════════════════════════════════════════════
    // STATE VARIABLES
    // ═══════════════════════════════════════════════════════════════════════
    
    /// @notice Address of the platform owner (BlindHire admin)
    address public platformOwner;
    
    /// @notice Array of all deployed job contract addresses
    address[] public allJobs;
    
    /// @notice Mapping from job owner to their job contracts
    mapping(address => address[]) public jobsByOwner;
    
    /// @notice Mapping from job config hash to job contract address
    mapping(bytes32 => address) public jobByConfigHash;
    
    /// @notice Version of the factory contract
    string public constant VERSION = "1.0.0";
    
    // ═══════════════════════════════════════════════════════════════════════
    // EVENTS
    // ═══════════════════════════════════════════════════════════════════════
    
    /**
     * @notice Emitted when a new job is created
     * @param jobContract Address of the newly deployed JobContract
     * @param jobOwner Address of the job owner
     * @param jobConfigHash Hash of the job configuration
     * @param timestamp When the job was created
     */
    event JobCreated(
        address indexed jobContract,
        address indexed jobOwner,
        bytes32 indexed jobConfigHash,
        uint256 timestamp
    );
    
    // ═══════════════════════════════════════════════════════════════════════
    // MODIFIERS
    // ═══════════════════════════════════════════════════════════════════════
    
    /// @notice Only the platform owner can call this function
    modifier onlyPlatformOwner() {
        require(msg.sender == platformOwner, "Only platform owner");
        _;
    }
    
    // ═══════════════════════════════════════════════════════════════════════
    // CONSTRUCTOR
    // ═══════════════════════════════════════════════════════════════════════
    
    /**
     * @notice Initialize the JobFactory
     * @dev Sets the deployer as the platform owner
     */
    constructor() {
        platformOwner = msg.sender;
    }
    
    // ═══════════════════════════════════════════════════════════════════════
    // CORE FUNCTIONS
    // ═══════════════════════════════════════════════════════════════════════
    
    /**
     * @notice Create a new job contract
     * @dev Deploys a new JobContract instance for the job owner
     * @param jobConfigHash Hash of job configuration (job_id, requirements, etc.)
     * @param jobOwnerPubEncKey Job owner's public encryption key
     * @return job Address of the newly deployed JobContract
     */
    function createJob(
        bytes32 jobConfigHash,
        bytes memory jobOwnerPubEncKey
    ) external returns (address job) {
        require(jobConfigHash != bytes32(0), "Invalid config hash");
        require(jobByConfigHash[jobConfigHash] == address(0), "Job already exists");
        
        // Deploy new JobContract
        JobContract newJob = new JobContract(
            msg.sender,
            jobConfigHash,
            jobOwnerPubEncKey
        );
        
        job = address(newJob);
        
        // Track the new job
        allJobs.push(job);
        jobsByOwner[msg.sender].push(job);
        jobByConfigHash[jobConfigHash] = job;
        
        emit JobCreated(job, msg.sender, jobConfigHash, block.timestamp);
        
        return job;
    }
    
    // ═══════════════════════════════════════════════════════════════════════
    // VIEW FUNCTIONS
    // ═══════════════════════════════════════════════════════════════════════
    
    /**
     * @notice Get total number of jobs created
     * @return count Total number of job contracts deployed
     */
    function getTotalJobs() external view returns (uint256) {
        return allJobs.length;
    }
    
    /**
     * @notice Get all jobs created by a specific owner
     * @param owner Address of the job owner
     * @return jobs Array of job contract addresses
     */
    function getJobsByOwner(address owner) external view returns (address[] memory) {
        return jobsByOwner[owner];
    }
    
    /**
     * @notice Get number of jobs created by a specific owner
     * @param owner Address of the job owner
     * @return count Number of jobs owned
     */
    function getJobCountByOwner(address owner) external view returns (uint256) {
        return jobsByOwner[owner].length;
    }
    
    /**
     * @notice Get job contract address by config hash
     * @param configHash Hash of the job configuration
     * @return job Address of the job contract, or zero if not found
     */
    function getJobByConfigHash(bytes32 configHash) external view returns (address) {
        return jobByConfigHash[configHash];
    }
    
    /**
     * @notice Get job contract at a specific index
     * @param index Index in the allJobs array
     * @return job Address of the job contract
     */
    function getJobAt(uint256 index) external view returns (address) {
        require(index < allJobs.length, "Index out of bounds");
        return allJobs[index];
    }
    
    /**
     * @notice Check if a job exists for a given config hash
     * @param configHash Hash of the job configuration
     * @return exists Whether the job exists
     */
    function jobExists(bytes32 configHash) external view returns (bool) {
        return jobByConfigHash[configHash] != address(0);
    }
    
    // ═══════════════════════════════════════════════════════════════════════
    // ADMIN FUNCTIONS
    // ═══════════════════════════════════════════════════════════════════════
    
    /**
     * @notice Transfer platform ownership to a new address
     * @dev Only callable by current platform owner
     * @param newOwner Address of the new platform owner
     */
    function transferPlatformOwnership(address newOwner) external onlyPlatformOwner {
        require(newOwner != address(0), "Invalid new owner");
        platformOwner = newOwner;
    }
}
