from watercolour.tool import Tool

class ThresholdingValues(Tool):

    def __init__(self, path):
        super().__init__(path)
        self.ids.lbl.text = 'Values'

