# Edge Cases and Mitigations

This document outlines the potential edge cases for the AI-Powered Restaurant Recommendation System and how the architecture handles them to ensure reliability, cost control, and a good user experience.

## 1. Data Ingestion & Normalization
| Edge Case | Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| **Missing Data (Nulls)** | Filter crashes or LLM receives incomplete data. | The `pipeline.py` must impute missing numerical values (e.g., set rating to 0 or average) and use defaults for missing strings (e.g., "Unknown" for cuisine). |
| **Inconsistent Casing** | Location or cuisine matching fails. | The `SchemaNormalizer` should lowercase and trim all locations and cuisines during ingestion (e.g., "NEW DELHI" -> "new delhi"). |
| **Extreme Outliers** | Cost thresholds or rating bounds are broken. | Validate data bounds during ingestion (e.g., cap ratings to 5.0, enforce positive cost values). |

## 2. User Input & Filtering
| Edge Case | Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| **Zero Candidate Matches** | LLM prompt cannot be generated; user sees error. | The `FilterService` will intercept the empty result and immediately return a friendly message: *"No restaurants match your strict criteria. Try lowering the minimum rating or changing the budget."* Do not call the LLM API. |
| **Too Many Matches** | Exceeds LLM token limit, leading to API rejection and high costs. | Pre-sort the candidates by rating/votes and enforce a hard `MAX_CANDIDATES` cap (e.g., 30) before building the prompt. |
| **Extremely Long Free-Text Input** | User pastes an essay into `additional_preferences`, exceeding tokens or causing prompt injection. | Apply a strict character limit (e.g., 200 chars) on `additional_preferences` at the API/UI boundary. |
| **Fewer Matches than Requested `top_k`** | User asks for 5, but only 2 match the filters. | The orchestrator will pass the 2 candidates to the LLM and return a response with only 2 items. |

## 3. LLM Integration
| Edge Case | Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| **LLM Hallucinations** | LLM invents a non-existent restaurant or suggests one outside the filtered list. | Use strict prompting rules ("Only select from the provided JSON list"). The `ResponseParser` must validate that every `restaurant_id` returned by the LLM exists in the provided candidate set. If it doesn't, drop the hallucinated item. |
| **Malformed JSON Response** | The `ResponseParser` fails to parse the LLM output, breaking the app. | Enable `response_format={ "type": "json_object" }` if using OpenAI. Use a regex fallback to extract JSON blocks. If parsing completely fails, fallback to returning the top-K restaurants sorted by rating with a generic explanation. |
| **LLM Provider Timeout / 502** | Request hangs or fails, degrading user experience. | Implement a timeout (e.g., 15s) and a single retry with exponential backoff. If it still fails, gracefully fallback to the rating-based sorting without AI explanations. |
| **Rate Limiting (429 Error)** | API quotas exceeded. | The application should catch the `429` exception and notify the user to try again later. |

## 4. UI & Presentation (Streamlit / Web)
| Edge Case | Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| **Empty Required Fields** | Backend validation fails (400 Bad Request). | The UI must enforce `required` flags on Location, Budget, and Cuisine before allowing submission. |
| **Prolonged LLM Latency** | User thinks the app is frozen and clicks submit multiple times. | The UI must show a clear, blocking loading spinner (`st.spinner`) and disable the submit button while waiting for the orchestrator. |
