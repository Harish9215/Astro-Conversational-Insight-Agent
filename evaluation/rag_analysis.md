# RAG Evaluation

## Overview
The system uses intent-aware retrieval to decide when to query the astrology knowledge base. Retrieval is performed using sentence-transformer embeddings with FAISS vector search.

---

## Case 1: Retrieval Helped

**User Question**
Which planet affects my love life?

**Behavior**
The system detected a relationship related intent and retrieved information from `planetary_impacts.json`.

**Outcome**
The retrieved context provided grounded astrological facts about planetary influence on relationships, which helped the LLM generate a relevant and factual response.

**Conclusion**
Retrieval improved response grounding and reduced hallucination risk.

---

## Case 2: Retrieval Hurt

**User Question**
Summarize what we talked about so far.

**Behavior**
If retrieval were used, the system might fetch unrelated astrology documents.

**Outcome**
This would introduce irrelevant context and potentially confuse the model.

**Solution**
Retrieval is disabled for summary type queries and the system relies on conversation memory instead.

---

## Trade-offs

### Retrieval Always On
Pros:
- More grounded responses

Cons:
- Adds latency
- Can introduce irrelevant context
- Higher compute cost

### Intent-Aware Retrieval (Current Approach)

Pros:
- Lower latency
- Reduced hallucinations
- More relevant context usage

Cons:
- Requires accurate intent detection
- Some edge cases may skip useful retrieval

---

## Conclusion

Intent-aware retrieval combined with session based memory allows the chatbot to balance contextual grounding and conversation continuity while keeping inference costs manageable.