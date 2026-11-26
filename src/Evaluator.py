from .data_models import RagDataset, StudentSearchResults


class Evaluator:
    @staticmethod
    def evaluate_sources(
        student_search_results: StudentSearchResults,
        given_dataset: RagDataset) -> tuple[float, float, float, float]:
        ks = {
            1: [],
            3: [],
            5: [],
            10: []
        }
        for stud_question, answered_question in zip(
            student_search_results.search_results, given_dataset.rag_questions):
            
