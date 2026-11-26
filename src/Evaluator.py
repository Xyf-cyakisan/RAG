from .data_models import RagDataset, StudentSearchResults


class Evaluator:
    @staticmethod
    def evaluate_sources(
        student_search_results: StudentSearchResults,
            given_dataset: RagDataset
                        ) -> list[float]:
        ks = {
            1: [],
            3: [],
            5: [],
            10: []
        }
        for (stud_question,
             answered_question) in zip(student_search_results.search_results,
                                       given_dataset.rag_questions):
            if stud_question.question_id != answered_question.question_id:
                raise ValueError("Evaluation cannot proceed because of "
                                 "comparaison between differents questions"
                                 f"IDS ('{stud_question.question_id}' != "
                                 f"'{answered_question.question_id}')")
            for k in ks.keys():
                key_k = k
                if k > len(stud_question.retrieved_sources):
                    k = len(stud_question.retrieved_sources)
                to_check = stud_question.retrieved_sources[:k]
                min_cross = False
                for source in to_check:
                    if (source.file_path
                       != answered_question.sources[0].file_path):
                        continue
                    else:
                        answer_source = answered_question.sources[0]
                        intersection = max(
                            0,
                            min(source.last_character_index,
                                answer_source.last_character_index)
                            - max(source.first_character_index,
                                  answer_source.first_character_index)
                        )
                        length_stud = (source.last_character_index
                                       - source.first_character_index)
                        length_answer = (answer_source.last_character_index
                                         - answer_source.first_character_index)
                        union = (length_answer + length_stud) - intersection
                        if intersection == 0:
                            continue
                        else:
                            if intersection / union >= 0.05:
                                min_cross = True
                ks[key_k].append(min_cross)
        for key_k in ks.keys():
            ks[key_k] = round(float(len([bool for bool in ks[key_k]
                                         if bool is True])
                                    / len(ks[key_k])), 2)
        return list(ks.values())
