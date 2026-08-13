from src.query.planner import QueryPlanner


class QueryService:

    def __init__(
        self,
        planner: QueryPlanner,
        sql_generator,
        answer_generator,
        databricks,
        web_search=None,
    ):
        self.planner = planner
        self.sql_generator = sql_generator
        self.answer_generator = answer_generator
        self.databricks = databricks
        self.web_search = web_search

    def ask(self, question: str):

        plan = self.planner.plan(question)

        print(f"Route: {plan.route}")
        print(f"Intent: {plan.intent}")

        if plan.route == "database":
            return self.database_flow(question, plan)

        elif plan.route == "web":
            return self.web_flow(question, plan)

        elif plan.route == "hybrid":
            return self.hybrid_flow(question, plan)

        else:
            raise ValueError(
                f"Unsupported query route: {plan.route}"
            )

    # ====================================
    # DATABASE FLOW
    # ====================================

    def database_flow(self, question: str, plan):

        sql = self.sql_generator.generate_sql(
            question=question,
        )

        print("\nGenerated SQL:")
        print(sql)

        result = self.databricks.execute_query(sql)

        print("\nDatabricks Result:")
        print(result)

        answer = self.answer_generator.generate_answer(
            question=question,
            query=sql,
            database_result=result,
        )

        return {
            "answer": answer,
            "route": plan.route,
            "intent": plan.intent,
            "sql": sql,
            "result": result,
            "sources": [],
        }

    # ====================================
    # WEB FLOW
    # ====================================

    def web_flow(self, question: str, plan):

        if self.web_search is None:
            raise RuntimeError(
                "WebSearch has not been configured."
            )

        web_result = self.web_search.search(question)

        print("\nWeb Results:")
        print(web_result)

        answer = self.answer_generator.generate_answer(
            question=question,
            web_result=web_result,
        )

        return {
            "answer": answer,
            "route": plan.route,
            "intent": plan.intent,
            "sql": None,
            "result": None,
            "sources": web_result,
        }

    # ====================================
    # HYBRID FLOW
    # ====================================

    def hybrid_flow(self, question: str, plan):

        if self.web_search is None:
            raise RuntimeError(
                "WebSearch has not been configured."
            )

        # --------------------------------
        # DATABASE
        # --------------------------------

        sql = self.sql_generator.generate_sql(
            question=question,
        )

        print("\nGenerated SQL:")
        print(sql)

        db_result = self.databricks.execute_query(sql)

        print("\nDatabricks Result:")
        print(db_result)

        # --------------------------------
        # WEB
        # --------------------------------

        web_result = self.web_search.search(question)

        print("\nWeb Results:")
        print(web_result)

        # --------------------------------
        # FINAL ANSWER
        # --------------------------------

        answer = self.answer_generator.generate_answer(
            question=question,
            query=sql,
            database_result=db_result,
            web_result=web_result,
        )

        return {
            "answer": answer,
            "route": plan.route,
            "intent": plan.intent,
            "sql": sql,
            "result": db_result,
            "sources": web_result,
        }