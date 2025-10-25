import pytest
import hashlib
import json
from hashing import compute_hashes, sha256_hash


class TestComputeHashes:
    """Test the compute_hashes function"""
    
    def test_compute_hashes_basic(self):
        """Test basic hash computation"""
        job_id = "test_job_123"
        score = 0.85
        decision = "auto_pass"
        model_id = "test_model_v1"
        resume_text = "test resume content"
        
        resume_hash, model_hash, score_hash = compute_hashes(
            job_id=job_id,
            score=score,
            decision=decision,
            model_id=model_id,
            resume_text=resume_text
        )
        
        # All hashes should be hex strings
        assert isinstance(resume_hash, str)
        assert isinstance(model_hash, str)
        assert isinstance(score_hash, str)
        
        # All hashes should be 64 characters (SHA256)
        assert len(resume_hash) == 64
        assert len(model_hash) == 64
        assert len(score_hash) == 64
        
        # All should be valid hex
        int(resume_hash, 16)
        int(model_hash, 16)
        int(score_hash, 16)
    
    def test_compute_hashes_deterministic(self):
        """Test that hashes are deterministic"""
        job_id = "test_job_123"
        score = 0.85
        decision = "auto_pass"
        model_id = "test_model_v1"
        resume_text = "test resume content"
        
        # Compute hashes twice
        result1 = compute_hashes(job_id, score, decision, model_id, resume_text)
        result2 = compute_hashes(job_id, score, decision, model_id, resume_text)
        
        # Should be identical
        assert result1 == result2
    
    def test_compute_hashes_different_inputs(self):
        """Test that different inputs produce different hashes"""
        base_args = {
            "job_id": "test_job_123",
            "score": 0.85,
            "decision": "auto_pass",
            "model_id": "test_model_v1",
            "resume_text": "test resume content"
        }
        
        base_result = compute_hashes(**base_args)
        
        # Different job_id should produce different score_hash
        different_job = base_args.copy()
        different_job["job_id"] = "different_job"
        different_job_result = compute_hashes(**different_job)
        assert base_result[2] != different_job_result[2]  # score_hash different
        
        # Different score should produce different score_hash
        different_score = base_args.copy()
        different_score["score"] = 0.75
        different_score_result = compute_hashes(**different_score)
        assert base_result[2] != different_score_result[2]  # score_hash different
        
        # Different decision should produce different score_hash
        different_decision = base_args.copy()
        different_decision["decision"] = "review"
        different_decision_result = compute_hashes(**different_decision)
        assert base_result[2] != different_decision_result[2]  # score_hash different
        
        # Different model_id should produce different model_hash and score_hash
        different_model = base_args.copy()
        different_model["model_id"] = "different_model"
        different_model_result = compute_hashes(**different_model)
        assert base_result[1] != different_model_result[1]  # model_hash different
        assert base_result[2] != different_model_result[2]  # score_hash different
        
        # Different resume_text should produce different resume_hash and score_hash
        different_resume = base_args.copy()
        different_resume["resume_text"] = "different resume content"
        different_resume_result = compute_hashes(**different_resume)
        assert base_result[0] != different_resume_result[0]  # resume_hash different
        assert base_result[2] != different_resume_result[2]  # score_hash different
    
    def test_score_rounding(self):
        """Test that score is properly rounded to 4 decimal places"""
        args = {
            "job_id": "test_job",
            "score": 0.123456789,  # More than 4 decimal places
            "decision": "review",
            "model_id": "test_model",
            "resume_text": "test content"
        }
        
        result1 = compute_hashes(**args)
        
        # Change to score that rounds to the same value
        args["score"] = 0.123456999
        result2 = compute_hashes(**args)
        
        # Should produce same score_hash due to rounding
        assert result1[2] == result2[2]
        
        # But different enough score should produce different hash
        args["score"] = 0.123556789  # Changed to have more significant difference
        result3 = compute_hashes(**args)
        assert result1[2] != result3[2]
    
    def test_score_hash_json_structure(self):
        """Test that score hash uses correct JSON structure"""
        job_id = "test_job"
        score = 0.8567
        decision = "auto_pass"
        model_id = "test_model"
        resume_text = "test content"
        
        # Manually compute what the score hash should be
        resume_hash = hashlib.sha256(resume_text.encode('utf-8')).hexdigest()
        model_hash = hashlib.sha256(model_id.encode('utf-8')).hexdigest()
        
        expected_payload = json.dumps({
            "job_id": job_id,
            "similarity_score": round(score, 4),
            "decision": decision,
            "model_hash": model_hash,
            "resume_hash": resume_hash
        }, sort_keys=True, separators=(',', ':'))
        
        expected_score_hash = hashlib.sha256(expected_payload.encode('utf-8')).hexdigest()
        
        _, _, actual_score_hash = compute_hashes(job_id, score, decision, model_id, resume_text)
        
        assert actual_score_hash == expected_score_hash
    
    def test_empty_inputs(self):
        """Test behavior with empty string inputs"""
        result = compute_hashes("", 0.0, "", "", "")
        
        assert len(result) == 3
        assert all(isinstance(h, str) and len(h) == 64 for h in result)
    
    def test_unicode_inputs(self):
        """Test with Unicode characters in inputs"""
        job_id = "测试工作"
        decision = "révision"
        model_id = "modelo_español"
        resume_text = "contenu français avec accents éàü"
        score = 0.75
        
        result = compute_hashes(job_id, score, decision, model_id, resume_text)
        
        assert len(result) == 3
        assert all(isinstance(h, str) and len(h) == 64 for h in result)
    
    def test_extreme_score_values(self):
        """Test with extreme score values"""
        base_args = {
            "job_id": "test",
            "decision": "review",
            "model_id": "test_model",
            "resume_text": "test"
        }
        
        # Test with score 0.0
        result_zero = compute_hashes(score=0.0, **base_args)
        assert len(result_zero) == 3
        
        # Test with score 1.0
        result_one = compute_hashes(score=1.0, **base_args)
        assert len(result_one) == 3
        
        # They should be different
        assert result_zero[2] != result_one[2]


class TestSha256Hash:
    """Test the sha256_hash utility function"""
    
    def test_sha256_hash_basic(self):
        """Test basic SHA256 hashing"""
        text = "hello world"
        result = sha256_hash(text)
        
        # Should return hex string of length 64
        assert isinstance(result, str)
        assert len(result) == 64
        
        # Should be valid hex
        int(result, 16)
        
        # Should match expected hash
        expected = hashlib.sha256(text.encode('utf-8')).hexdigest()
        assert result == expected
    
    def test_sha256_hash_deterministic(self):
        """Test that SHA256 hash is deterministic"""
        text = "test string for hashing"
        
        result1 = sha256_hash(text)
        result2 = sha256_hash(text)
        
        assert result1 == result2
    
    def test_sha256_hash_different_inputs(self):
        """Test that different inputs produce different hashes"""
        text1 = "hello"
        text2 = "world"
        
        hash1 = sha256_hash(text1)
        hash2 = sha256_hash(text2)
        
        assert hash1 != hash2
    
    def test_sha256_hash_empty_string(self):
        """Test SHA256 hash of empty string"""
        result = sha256_hash("")
        
        assert isinstance(result, str)
        assert len(result) == 64
        
        # Should match known hash of empty string
        expected = hashlib.sha256(b"").hexdigest()
        assert result == expected
    
    def test_sha256_hash_unicode(self):
        """Test SHA256 hash with Unicode characters"""
        text = "Hello 世界 🌍 café naïve résumé"
        result = sha256_hash(text)
        
        assert isinstance(result, str)
        assert len(result) == 64
        
        # Should match manual calculation
        expected = hashlib.sha256(text.encode('utf-8')).hexdigest()
        assert result == expected
    
    def test_sha256_hash_long_text(self):
        """Test SHA256 hash with very long text"""
        long_text = "a" * 10000
        result = sha256_hash(long_text)
        
        assert isinstance(result, str)
        assert len(result) == 64


class TestHashIntegrity:
    """Test hash integrity and consistency"""
    
    def test_hash_consistency_across_calls(self):
        """Test that hashes remain consistent across multiple calls"""
        test_cases = [
            {
                "job_id": "job_1",
                "score": 0.85,
                "decision": "auto_pass",
                "model_id": "model_v1",
                "resume_text": "software engineer python"
            },
            {
                "job_id": "job_2",
                "score": 0.45,
                "decision": "review",
                "model_id": "model_v2",
                "resume_text": "data scientist machine learning"
            }
        ]
        
        # Store first results
        first_results = []
        for case in test_cases:
            result = compute_hashes(**case)
            first_results.append(result)
        
        # Compute again and compare
        for i, case in enumerate(test_cases):
            result = compute_hashes(**case)
            assert result == first_results[i]
    
    def test_hash_collision_resistance(self):
        """Test that similar inputs produce different hashes"""
        base_text = "software engineer with python experience"
        
        # Generate multiple similar texts
        variations = [
            base_text,
            base_text + " ",  # Extra space
            base_text + ".",  # Extra punctuation
            base_text.replace("python", "Python"),  # Case change
            base_text.replace(" ", "  "),  # Double space
        ]
        
        hashes = []
        for text in variations:
            hash_result = sha256_hash(text)
            hashes.append(hash_result)
        
        # All hashes should be different
        assert len(set(hashes)) == len(hashes)
    
    def test_cross_component_hash_independence(self):
        """Test that changing one component doesn't affect unrelated hashes"""
        base_args = {
            "job_id": "test_job",
            "score": 0.75,
            "decision": "review",
            "model_id": "test_model",
            "resume_text": "test resume"
        }
        
        base_resume_hash, base_model_hash, base_score_hash = compute_hashes(**base_args)
        
        # Changing only job_id should only affect score_hash
        modified_args = base_args.copy()
        modified_args["job_id"] = "different_job"
        mod_resume_hash, mod_model_hash, mod_score_hash = compute_hashes(**modified_args)
        
        assert mod_resume_hash == base_resume_hash  # Should be same
        assert mod_model_hash == base_model_hash    # Should be same
        assert mod_score_hash != base_score_hash    # Should be different
        
        # Changing only model_id should affect model_hash and score_hash
        modified_args = base_args.copy()
        modified_args["model_id"] = "different_model"
        mod_resume_hash, mod_model_hash, mod_score_hash = compute_hashes(**modified_args)
        
        assert mod_resume_hash == base_resume_hash  # Should be same
        assert mod_model_hash != base_model_hash    # Should be different
        assert mod_score_hash != base_score_hash    # Should be different


if __name__ == "__main__":
    pytest.main([__file__])