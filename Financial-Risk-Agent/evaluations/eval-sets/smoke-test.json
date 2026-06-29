{
  "version": "1.0",
  "id": "smoke-test",
  "name": "Smoke Test",
  "evaluatorRefs": ["LLMJudgeTrajectoryEvaluator"],
  "evaluations": [
    {
      "id": "test-1",
      "name": "Assess UiPath",
      "inputs": {
        "company_name": "UiPath Inc.",
        "country": "USA"
      },
      "evaluationCriterias": {
        "LLMJudgeTrajectoryEvaluator": {
          "expectedAgentBehavior": "Agent should return a risk assessment with a score and category for UiPath Inc."
        }
      }
    }
  ]
}
