# Technical Documentation - Part 2
## Continuation of Use Cases, Conclusions & Future Work

### 7.2 Case 2: Symptom-Based Diagnosis - Brake Noise

**Initial Input**:
```
Mechanic: "Customer says the car makes a loud squealing noise when braking, 
Honda Civic 2020, about 45,000 miles"
```

**Agent Actions**:
1. RAG retrieval finds similar symptom
2. Provides probable causes with percentages
3. Asks diagnostic follow-up questions
4. Confirms diagnosis based on answers
5. Finds parts and calculates cost

**Outcome**: Complete brake pad replacement estimate in under 2 minutes.

---

### 7.3 Case 3: Known Issues Query

**Scenario**: Mechanic wants to check common problems before diagnosis.

**Conversation**:
```
Mechanic: "What are common issues with Nissan Sentra 2018?"

[Tool: query_known_issues]
Input: {"brand": "Nissan", "model": "Sentra", "year": 2018}

Result: {
  "issues_found": 2,
  "common_issues": [
    {
      "issue": "CVT transmission failure",
      "frequency": "Common",
      "symptoms": ["Shuddering", "Delayed engagement"],
      "note": "Extended warranty available"
    },
    {
      "issue": "Oxygen sensor failure",
      "frequency": "Moderate",
      "symptoms": ["Check engine light", "Poor fuel economy"]
    }
  ]
}
