import json
from common.data.zero_trust_consts import *
from monkey_island.cc.models.finding import Finding


def get_all_findings():
    all_findings = Finding.objects()
    enriched_findings = [get_enriched_finding(f) for f in all_findings]
    return enriched_findings


def get_events_as_dict(events):
    return [json.loads(event.to_json()) for event in events]


def get_enriched_finding(finding):
    test_info = TESTS_MAP[finding.test]
    enriched_finding = {
        # TODO add test explanation per status.
        "test": test_info[EXPLANATION_KEY],
        "pillars": test_info[PILLARS_KEY],
        "status": finding.status,
        "events": get_events_as_dict(finding.events)
    }
    return enriched_finding


def get_lcd_worst_status_for_test(all_findings_for_test):
    current_status = STATUS_UNEXECUTED
    for finding in all_findings_for_test:
        if TEST_STATUSES.index(finding.status) < TEST_STATUSES.index(current_status):
            current_status = finding.status

    return current_status


def get_tests_status(directive_tests):
    results = []
    for test in directive_tests:
        test_findings = Finding.objects(test=test)
        results.append(
            {
                "test": test,
                "status": get_lcd_worst_status_for_test(test_findings)
            }
        )
    return results


def get_directive_status(directive_tests):
    worst_status = STATUS_UNEXECUTED
    all_statuses = set()
    for test in directive_tests:
        all_statuses |= set(Finding.objects(test=test).distinct("status"))

    for status in all_statuses:
        if TEST_STATUSES.index(status) < TEST_STATUSES.index(worst_status):
            worst_status = status

    return worst_status


def get_directives_status():
    all_directive_statuses = {}

    # init with empty lists
    for pillar in PILLARS:
        all_directive_statuses[pillar] = []

    for directive, directive_tests in DIRECTIVES_TO_TESTS.items():
        for pillar in DIRECTIVES_TO_PILLARS[directive]:
            all_directive_statuses[pillar].append(
                {
                    "directive": directive,
                    "tests": get_tests_status(directive_tests),
                    "status": get_directive_status(directive_tests)
                }
            )

    return all_directive_statuses


def get_pillar_grade(pillar, all_findings):
    pillar_grade = {
        "pillar": pillar,
        STATUS_CONCLUSIVE: 0,
        STATUS_INCONCLUSIVE: 0,
        STATUS_POSITIVE: 0,
        STATUS_UNEXECUTED: 0
    }

    tests_of_this_pillar = PILLARS_TO_TESTS[pillar]

    test_unexecuted = {}
    for test in tests_of_this_pillar:
        test_unexecuted[test] = True

    for finding in all_findings:
        test_unexecuted[finding.test] = False
        test_info = TESTS_MAP[finding.test]
        if pillar in test_info[PILLARS_KEY]:
            pillar_grade[finding.status] += 1

    pillar_grade[STATUS_UNEXECUTED] = sum(1 for condition in test_unexecuted.values() if condition)

    return pillar_grade


def get_pillars_grades():
    pillars_grades = []
    all_findings = Finding.objects()
    for pillar in PILLARS:
        pillars_grades.append(get_pillar_grade(pillar, all_findings))
    return pillars_grades
