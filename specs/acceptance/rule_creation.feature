Feature: Rule creation, testing, review, and activation
  As a policy author
  I want to create and test declarative rules before enabling them
  So that rules do not produce unexpected production impact

  Scenario: Create, test, review, and enable a rule
    Given a policy author drafts a rule named "political-review" with trigger "on_content_create" and condition matching metadata.topics contains "politics"
    When the author runs the rule against a sandbox sample that has metadata.topics = ["politics"]
    Then the test harness reports at least one matching example
    When a reviewer approves the rule with summary "ok for rollout"
    Then the rule is stored with `enabled=true` and `priority` preserved
    When new content is created that matches the rule trigger and conditions
    Then a `rule_match` event is recorded with `rule_id` and `content_id` and the configured action `require_human_review` is emitted

  Scenario: Reject unsafe rule referencing unknown field
    Given a policy author drafts a rule that references non_existent_field
    When the system validates the rule syntax
    Then the rule save is rejected with a validation error explaining the missing field
