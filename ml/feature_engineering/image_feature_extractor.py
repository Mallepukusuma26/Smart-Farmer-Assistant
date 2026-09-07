"""
Computer Vision Image Feature Extractor Module for Smart Farmer Assistant.

Processes plant leaf images entirely offline using Pillow, OpenCV, NumPy, and Scikit-Learn.
Performs image loading, validation, resizing, normalization, color space conversion (RGB, HSV),
color histogram calculation, GLCM texture descriptor extraction (contrast, homogeneity, energy),
Sobel edge response density, and Hu shape moment invariants.
"""

from typing import Dict, Any, List, Tuple, Optional
import cv2
import numpy as np
from PIL import Image
import os
import logging

logger = logging.getLogger(__name__)


class ImageFeatureExtractor:
    """
    Offline Computer Vision feature extraction pipeline for plant leaf disease classification.
    Extracts 15 distinct color, texture, edge, and shape visual descriptors from leaf images.
    """

    def __init__(self, target_size: Tuple[int, int] = (128, 128)):
        self.target_size = target_size

    def load_and_preprocess_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Loads image file using Pillow, validates dimensions, resizes to target size,
        and converts to BGR numpy array for OpenCV processing.
        """
        if not os.path.exists(image_path):
            logger.error(f"Image path does not exist: {image_path}")
            return None

        try:
            # Pillow load for file integrity validation
            with Image.open(image_path) as pil_img:
                pil_img.verify()

            # OpenCV load
            img_bgr = cv2.imread(image_path)
            if img_bgr is None:
                logger.error(f"Failed to decode image at {image_path}")
                return None

            # Resize to standardized dimensions
            resized_bgr = cv2.resize(img_bgr, self.target_size, interpolation=cv2.INTER_AREA)
            return resized_bgr

        except Exception as e:
            logger.error(f"Error loading image {image_path}: {str(e)}")
            return None

    def extract_color_features(self, img_bgr: np.ndarray) -> Dict[str, float]:
        """
        Extracts RGB and HSV color space statistics (mean & standard deviation per channel).
        """
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

        r_mean, g_mean, b_mean = np.mean(img_rgb[:, :, 0]), np.mean(img_rgb[:, :, 1]), np.mean(img_rgb[:, :, 2])
        r_std, g_std, b_std = np.std(img_rgb[:, :, 0]), np.std(img_rgb[:, :, 1]), np.std(img_rgb[:, :, 2])

        h_mean, s_mean, v_mean = np.mean(img_hsv[:, :, 0]), np.mean(img_hsv[:, :, 1]), np.mean(img_hsv[:, :, 2])

        return {
            "mean_r": float(r_mean),
            "mean_g": float(g_mean),
            "mean_b": float(b_mean),
            "std_r": float(r_std),
            "std_g": float(g_std),
            "std_b": float(b_std),
            "mean_h": float(h_mean),
            "mean_s": float(s_mean),
            "mean_v": float(v_mean)
        }

    def extract_texture_features(self, img_bgr: np.ndarray) -> Dict[str, float]:
        """
        Extracts texture descriptors: GLCM contrast, homogeneity, energy, and Laplacian variance.
        """
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        # Laplacian variance measures image sharpness/texture coarseness
        laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())

        # Quantize gray image for texture co-occurrence matrix approximation
        quantized = (gray // 16).astype(np.uint8)
        h, w = quantized.shape

        # Co-occurrence matrix at distance 1, angle 0
        glcm = np.zeros((16, 16), dtype=np.float64)
        for i in range(h):
            for j in range(w - 1):
                i_val = quantized[i, j]
                j_val = quantized[i, j + 1]
                glcm[i_val, j_val] += 1.0

        total_pairs = np.sum(glcm)
        if total_pairs > 0:
            glcm /= total_pairs

        # Contrast: sum( (i - j)^2 * P(i,j) )
        contrast = 0.0
        homogeneity = 0.0
        energy = 0.0
        for i in range(16):
            for j in range(16):
                val = glcm[i, j]
                contrast += ((i - j) ** 2) * val
                homogeneity += val / (1.0 + abs(i - j))
                energy += val ** 2

        return {
            "glcm_contrast": float(contrast),
            "glcm_homogeneity": float(homogeneity),
            "glcm_energy": float(energy),
            "laplacian_var": float(laplacian_var)
        }

    def extract_edge_features(self, img_bgr: np.ndarray) -> Dict[str, float]:
        """
        Extracts Sobel edge density and Canny edge response statistics.
        """
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel_magnitude = np.sqrt(sobelx**2 + sobely**2)

        edge_density = float(np.mean(sobel_magnitude > 50))
        mean_edge_intensity = float(np.mean(sobel_magnitude))

        return {
            "sobel_edge_density": float(edge_density),
            "mean_edge_intensity": float(mean_edge_intensity)
        }

    def extract_shape_features(self, img_bgr: np.ndarray) -> Dict[str, float]:
        """
        Extracts Hu moment invariants for scale and rotation invariant shape representation.
        """
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        moments = cv2.moments(gray)
        hu_moments = cv2.HuMoments(moments).flatten()

        # Log scale Hu moments for numerical stability
        log_hu = []
        for h in hu_moments[:2]:
            val = -1.0 * np.copysign(1.0, h) * np.log10(abs(h) + 1e-10)
            log_hu.append(float(val))

        return {
            "hu_moment_1": log_hu[0],
            "hu_moment_2": log_hu[1]
        }

    def extract_all_features(self, image_path: str) -> Optional[np.ndarray]:
        """
        Runs complete computer vision pipeline, extracting a 15-element feature vector.
        """
        img_bgr = self.load_and_preprocess_image(image_path)
        if img_bgr is None:
            return None

        color_feat = self.extract_color_features(img_bgr)
        texture_feat = self.extract_texture_features(img_bgr)
        edge_feat = self.extract_edge_features(img_bgr)
        shape_feat = self.extract_shape_features(img_bgr)

        vector = [
            color_feat["mean_r"], color_feat["mean_g"], color_feat["mean_b"],
            color_feat["std_r"], color_feat["std_g"], color_feat["std_b"],
            color_feat["mean_h"], color_feat["mean_s"], color_feat["mean_v"],
            texture_feat["glcm_contrast"], texture_feat["glcm_homogeneity"], texture_feat["glcm_energy"],
            edge_feat["sobel_edge_density"], shape_feat["hu_moment_1"], shape_feat["hu_moment_2"]
        ]

        return np.array(vector, dtype=np.float32)
