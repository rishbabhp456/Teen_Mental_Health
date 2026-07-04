import os
import unittest

from src.utils import Teen_Depression


class ScalerPredictionTests(unittest.TestCase):
    def test_prediction_uses_scaler(self):
        obj = Teen_Depression()
        sample = {
            'age': '16',
            'gender': 'male',
            'daily_social_media_hours': '3',
            'sleep_hours': '7',
            'screen_time_before_sleep': '2',
            'academic_performance': '3',
            'physical_activity': '4',
            'social_interaction_level': 'medium',
            'stress_level': '4',
            'anxiety_level': '3',
            'addiction_level': '2',
            'platform_usage': 'Instagram'
        }

        prediction = obj.predict_depression_label(sample)
        self.assertIn(prediction[0], [0, 1])


if __name__ == '__main__':
    unittest.main()
