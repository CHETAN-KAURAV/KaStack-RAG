# answer_generator.py

def generate_answer(query, docs):

    query_lower = query.lower()

    # =====================================================
    # PERSONA QUESTIONS
    # =====================================================

    if (
            "kind of person" in query_lower
            or "personality" in query_lower
            or "who is this user" in query_lower
    ):

        traits = []
        occupations = []

        for doc in docs:

            if doc["type"] == "persona":

                metadata = doc["metadata"]

                occupations.extend(
                    metadata.get(
                        "occupation",
                        []
                    )
                )

                for trait in metadata.get(
                        "traits",
                        []
                ):

                    traits.append(
                        trait["trait"]
                    )

        occupations = list(
            set(occupations)
        )

        traits = list(
            set(traits)
        )

        if not traits and not occupations:

            return (
                "No strong persona information "
                "was found."
            )

        answer = (
            "Based on retrieved conversations, "
            "the user appears to be:\n\n"
        )

        if traits:

            answer += (
                "Traits:\n"
            )

            for t in traits[:10]:

                answer += (
                    f"• {t}\n"
                )

        if occupations:

            answer += (
                "\nOccupations mentioned:\n"
            )

            for occ in occupations[:10]:

                answer += (
                    f"• {occ}\n"
                )

        return answer

    # =====================================================
    # HOBBIES
    # =====================================================

    elif (
            "hobbies" in query_lower
            or "interests" in query_lower
            or "likes" in query_lower
    ):

        hobbies = []

        for doc in docs:

            if doc["type"] == "persona":

                hobbies.extend(
                    doc["metadata"].get(
                        "hobbies",
                        []
                    )
                )

        hobbies = list(
            set(hobbies)
        )

        if not hobbies:

            return (
                "No hobbies were found."
            )

        answer = (
            "The user appears to enjoy:\n\n"
        )

        for hobby in hobbies[:15]:

            answer += (
                f"• {hobby}\n"
            )

        return answer

    # =====================================================
    # COMMUNICATION STYLE
    # =====================================================

    elif (
            "talk" in query_lower
            or "communicate" in query_lower
            or "communication" in query_lower
            or "speak" in query_lower
    ):

        styles = []

        for doc in docs:

            if doc["type"] == "persona":

                styles.append(
                    doc["metadata"].get(
                        "communication_style",
                        {}
                    )
                )

        if not styles:

            return (
                "No communication data found."
            )

        avg_words = sum(
            s.get(
                "avg_words",
                0
            )
            for s in styles
        ) / len(styles)

        avg_questions = sum(
            s.get(
                "question_ratio",
                0
            )
            for s in styles
        ) / len(styles)

        avg_exclamations = sum(
            s.get(
                "exclamation_ratio",
                0
            )
            for s in styles
        ) / len(styles)

        return f"""
Communication Style

Average words per message:
{avg_words:.2f}

Question ratio:
{avg_questions:.2f}

Exclamation ratio:
{avg_exclamations:.2f}

The user generally appears conversational,
friendly and interactive.
"""

    # =====================================================
    # FALLBACK
    # =====================================================

    else:

        answer = (
            "Top Retrieved Information:\n\n"
        )

        for doc in docs[:5]:

            answer += (
                f"[{doc['type']}] "
                f"{doc['text']}\n\n"
            )

        return answer