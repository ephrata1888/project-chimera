Feature: Content creation, validation, approval, and publishing
  As an operator
  I want agent-generated content to flow through validation, approval, and publishing
  So that published content meets governance and quality standards

  Background:
    Given a running system with content, validation, and publish pipelines

  Scenario: Happy path — agent creates draft, validations pass, human approves, publish scheduled and executed
    Given agent "planner-1" creates a draft content with title "Explainer" and body "Short explainer about AI"
    When the system normalizes the draft into a `content` record
    And automated checks are run (toxicity, copyright, brand-safety)
    And all checks return status "pass"
    Then the `content.status` is "approved"
    When a publisher schedules the content for channel "twitter" at "2026-02-07T10:00:00Z"
    Then a `publish_log` entry exists with `content_id` equal to the draft id and `status` equal to "scheduled"
    When the scheduled time occurs and the external channel responds with success
    Then the `publish_log.status` is "published" and `publish_log.published_at` is set

  Scenario: Validation failure — draft flagged and requires human review
    Given agent "planner-1" creates a draft content with body "Contains badword1"
    When automated checks are run and at least one check returns status "fail"
    Then the `content.status` is "pending_review"
    And a `validation` record exists with `issues` listing the failing checks
    When a reviewer marks the content as "rejected" with reason "policy violation"
    Then the `content.status` is "rejected" and the `validation.status` is "rejected"
