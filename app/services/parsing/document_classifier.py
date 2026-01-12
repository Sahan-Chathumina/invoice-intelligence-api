class DocumentClassifier:
    @staticmethod
    def classify(text: str) -> str:
        keywords = ["invoice", "total", "amount", "tax", "bill"]
        text_lower = text.lower()

        for word in keywords:
            if word in text_lower:
                return "invoice"

        return "generic"
