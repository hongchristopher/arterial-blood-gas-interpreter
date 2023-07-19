class ABGInterpreter:
    """Blood gas interpreter, takes arguments for ph, co2, hco3, potassium, and spo2 values. Has methods for classifying each value (ph_classifier() and peripheral_classifier()) 
    and a method for main_interpretation(). Gets called by the '/interpret' POST route.
    """
    def __init__(self, ph, co2, hco3, potassium, spo2):
        self._ph = ph
        self._co2 = co2
        self._hco3 = hco3
        self._potassium = potassium
        self._spo2 = spo2
        
        self._potassium_result = None
        self._spo2_result = None
        self._final_result = None

    def ph_classifier(self):
        """General classifications for ph, co2, and hco3. Creates new attributes for each result. Needed to run main_interpretation().
        """
        if self._ph < 7.35:                          #pH Block - normal range: 7.35 - 7.45
            self._ph_result = "acidosis"
        elif self._ph > 7.45:
            self._ph_result = "alkalosis"
        else:
            self._ph_result = "normal"

        if self._co2 < 35:                           #Carbon Dioxide Block - normal range: 35-45
            self._co2_result = "low"
        elif self._co2 > 45:
            self._co2_result = "high"
        else:
            self._co2_result = "normal"

        if self._hco3 < 22:                          #Bicarbonate Block - normal range: 22-26
            self._hco3_result = "low"
        elif self._hco3 > 26:
            self._hco3_result = "high"
        else:
            self._hco3_result = "normal"

    def main_interpretation(self):
        """Interprets the results of the ph_classifier() method. Returns a final reading, if applicable.
        """
        key = (self._ph_result, self._co2_result, self._hco3_result)            
        
        interpretation_results = {
            ("normal", "normal", "normal"): "Normal Acid-Base State",               # (ph, co2, hco3) : final result

            ("acidosis", "high", "normal"): "Uncompensated Respiratory Acidosis",
            ("acidosis", "high", "high"): "Partially Compensated Respiratory Acidosis",
            ("normal", "high", "high"): "Fully Compensated Respiratory Acidosis",

            ("acidosis", "normal", "low"): "Uncompensated Metabolic Acidosis",
            ("acidosis", "high", "low"): "Partially Compensated Metabolic Acidosis",
            ("normal", "high", "low"): "Fully Compensated Respiratory Acidosis",

            ("alkalosis", "low", "normal"): "Uncompensated Respiratory Alkalosis",
            ("alkalosis", "low", "high"): "Partially Compensated Respiratory Alkalosis",
            ("normal", "low", "high"): "Fully Compensated Respiratory Alkalosis",

            ("alkalosis", "normal", "low"): "Uncompensated Metabolic Alkalosis",
            ("alkalosis", "high", "low"): "Partially Compensated Metabolic Alkalosis",
            ("normal", "high", "low"): "Fully Compensated Metabolic Alkalosis",
        }
        self._final_result = interpretation_results.get(key, "Unable to Interpret - Consider specimen contamination")     # Classifications not caught in the interpretation_results map are impossible.

        return self._final_result

    def peripheral_interpretation(self):
        """Directly interprets potassium and spo2 attributes, returns potassium and spo2 interpretations.
        """
        if 3.5 < self._potassium < 5:                           #Potassium Block
            self._potassium_result = "Normal"
        elif self._potassium < 3.5:
            self._potassium_result = "Hypokalemic"
        elif self._potassium > 5:
            self._potassium_result = "Hyperkalemic"
        else:
            self._potassium_result = "Unable to Interpret"

        if 94 < self._spo2 < 100:                               #SpO2 Block
            self._spo2_result = "Normal"
        elif self._spo2 < 94:
            self._spo2_result = "Hypoxemic"
        else:
            self._spo2_result = "Unable to Interpret"
        
        return [self._potassium_result, self._spo2_result]
