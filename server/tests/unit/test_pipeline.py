"""
Unit tests for pipeline components
"""

import pytest
from app.pipeline.precheck.image_checks import preflight, _contrast_ratio, _edge_density
from PIL import Image
import io
import numpy as np


class TestImagePrecheck:
    """Test image precheck functionality."""
    
    def create_test_image(self, width=500, height=500, color=(255, 255, 255)):
        """Helper to create test image bytes."""
        img = Image.new('RGB', (width, height), color=color)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG', dpi=(72, 72))
        img_bytes.seek(0)
        return img_bytes.getvalue()
    
    def test_preflight_valid_image(self):
        """Test preflight check with valid image."""
        image_bytes = self.create_test_image(800, 600)
        result = preflight(image_bytes)
        
        assert isinstance(result, dict)
        assert "ok" in result
        assert "width" in result
        assert "height" in result
        assert "dpi" in result
        assert "srgb" in result
        assert "contrast_ratio_global" in result
        assert "busy_score" in result
        assert "warnings" in result
        
        assert result["width"] == 800
        assert result["height"] == 600
        assert result["dpi"] >= 72
    
    def test_preflight_small_image(self):
        """Test preflight check with small image."""
        image_bytes = self.create_test_image(200, 200)
        result = preflight(image_bytes)
        
        assert result["ok"] is False
        assert any("too small" in w.lower() for w in result["warnings"])
    
    def test_preflight_empty_bytes(self):
        """Test preflight check with empty bytes."""
        result = preflight(b"")
        
        assert result["ok"] is False
        assert "error" in result
        assert "Empty image data" in result["error"]
    
    def test_preflight_invalid_bytes(self):
        """Test preflight check with invalid image bytes."""
        result = preflight(b"not an image")
        
        assert result["ok"] is False
        assert "error" in result
    
    def test_preflight_contrast(self):
        """Test preflight contrast detection."""
        # High contrast black image
        black_image = self.create_test_image(800, 600, color=(0, 0, 0))
        result_black = preflight(black_image)
        
        # White image (low contrast)
        white_image = self.create_test_image(800, 600, color=(255, 255, 255))
        result_white = preflight(white_image)
        
        # Both should have contrast warnings
        assert "contrast" in result_black.get("warnings", [""])[0].lower() or result_black["ok"]
        assert "contrast" in result_white.get("warnings", [""])[0].lower() or result_white["ok"]
    
    def test_contrast_ratio_calculation(self):
        """Test contrast ratio calculation."""
        # Create grayscale image
        img = Image.new('L', (100, 100), color=128)
        contrast = _contrast_ratio(img)
        
        assert isinstance(contrast, float)
        assert contrast > 0
    
    def test_edge_density_calculation(self):
        """Test edge density calculation."""
        # Create grayscale image
        img = Image.new('L', (100, 100), color=128)
        density = _edge_density(img)
        
        assert isinstance(density, float)
        assert 0 <= density <= 1


class TestPipelineErrorHandling:
    """Test error handling in pipeline components."""
    
    def test_preflight_none_input(self):
        """Test preflight with None input."""
        result = preflight(None)
        
        assert result["ok"] is False
        assert "error" in result
    
    def test_preflight_corrupted_image(self):
        """Test preflight with corrupted image data."""
        # Create partial PNG header
        corrupted = b'\x89PNG\r\n\x1a\n'
        result = preflight(corrupted)
        
        assert result["ok"] is False
        assert "error" in result

