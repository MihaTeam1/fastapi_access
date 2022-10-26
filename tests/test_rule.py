import pytest
from fastapi_access import Rule, AccessControl


test_user = {
    'username': 'admin',
    'age': 25,
    'roles': ['admin', 'staff'],
    'roles_with_names': [
        {'slug': 'admin', 'name': 'admin_test_name'},
        {'slug': 'staff', 'name': 'staff_test_name'},
    ],
    'organization_id': 5,
    'balance': 0,
    'income': 100,
}


def test_equal_true():
    rules = Rule('username') == 'admin'
    assert rules(test_user)
    rules = Rule('age') == 25
    assert rules(test_user)


def test_equal_false():
    rules = Rule('username') == 'test'
    assert not rules(test_user)
    rules = Rule('age') == 24
    assert not rules(test_user)


def test_not_equal_true():
    rules = Rule('username') != 'test'
    assert rules(test_user)
    rules = Rule('age') != 24
    assert rules(test_user)


def test_not_equal_false():
    rules = Rule('username') != 'admin'
    assert not rules(test_user)
    rules = Rule('age') != 25
    assert not rules(test_user)


def test_gt_true():
    rules = Rule('age') > 24
    assert rules(test_user)


def test_gt_false():
    rules = Rule('age') > 25
    assert not rules(test_user)
    rules = Rule('age') > 30
    assert not rules(test_user)


def test_lt_true():
    rules = Rule('age') < 30
    assert rules(test_user)


def test_lt_rule_false():
    rules = Rule('age') < 25
    assert not rules(test_user)
    rules = Rule('age') < 20
    assert not rules(test_user)


def test_gte_true():
    rules = Rule('age') >= 25
    assert rules(test_user)
    rules = Rule('age') >= 20
    assert rules(test_user)


def test_gte_false():
    rules = Rule('age') >= 26
    assert not rules(test_user)


def test_lte_true():
    rules = Rule('age') <= 25
    assert rules(test_user)
    rules = Rule('age') <= 30
    assert rules(test_user)


def test_lte_false():
    rules = Rule('age') <= 24
    assert not rules(test_user)


def test_contains_true():
    rules = Rule('roles').contains('staff')
    assert rules(test_user)


def test_contains_false():
    rules = Rule('roles').contains('test')
    assert not rules(test_user)


def test_not_contains_true():
    rules = Rule('roles').not_contains('test')
    assert rules(test_user)


def test_not_contains_false():
    rules = Rule('roles').not_contains('admin')
    assert not rules(test_user)


def test_in_true():
    rules = Rule('organization_id').in_([4,5,6])
    assert rules(test_user)


def test_in_false():
    rules = Rule('organization_id').in_([4, 6])
    assert not rules(test_user)


def test_not_in_true():
    rules = Rule('organization_id').not_in_([4,6])
    assert rules(test_user)


def test_not_in_false():
    rules = Rule('organization_id').not_in_([4,5,6])
    assert not rules(test_user)


def test_deep_path_true():
    rules = Rule('roles_with_names', 'slug').contains('admin')
    assert rules(test_user)
    rules = Rule('roles_with_names', 'name').contains('admin_test_name')
    assert rules(test_user)


def test_deep_path_false():
    rules = Rule('roles_with_names', 'slug').contains('admin_test_name')
    assert not rules(test_user)
    rules = Rule('roles_with_names', 'name').contains('admin')
    assert not rules(test_user)


def test_deep_values_list():
    rules = Rule('roles_with_names', 'slug')
    assert rules(test_user) == ['admin', 'staff']
    rules = Rule('roles_with_names', 'name')
    assert rules(test_user) == ['admin_test_name', 'staff_test_name']


def test_and_true():
    rules = Rule('income') & 1
    assert rules(test_user)


def test_and_false():
    rules = Rule('income') & 0
    assert not rules(test_user)
    rules = Rule('balance') & 1
    assert not rules(test_user)


def test_or_true():
    rules = Rule('balance') | 1
    assert rules(test_user)
    rules = Rule('income') | 0
    assert rules(test_user)


def test_or_false():
    rules = Rule('balance') | 0
    assert not rules(test_user)


def test_and_rules_true():
    rules = (
        (Rule('username') == 'admin')
        & (Rule('age') > 20)
    )
    assert rules(test_user)


def test_and_rules_false():
    rules = (
        (Rule('username') == 'test')
        & (Rule('age') > 20)
    )
    assert not rules(test_user)
    rules = (
        (Rule('username') == 'admin')
        & (Rule('age') > 25)
    )
    assert not rules(test_user)
    rules = (
        (Rule('username') == 'test')
        & (Rule('age') > 30)
    )
    assert not rules(test_user)


def test_or_rules_true():
    rules = (
        (Rule('username') == 'test')
        | (Rule('age') > 20)
    )
    assert rules(test_user)
    rules = (
        (Rule('username') == 'admin')
        | (Rule('age') > 30)
    )
    assert rules(test_user)
    rules = (
        (Rule('username') == 'admin')
        | (Rule('age') > 20)
    )
    assert rules(test_user)


def test_or_rules_false():
    rules = (
        (Rule('username') == 'test')
        | (Rule('age') > 30)
    )
    assert not rules(test_user)


def test_multi_conditions_true():
    rules = (
        (
            (Rule('username') == 'test')
            | (Rule('age') > 20)
        ) & Rule('roles').contains('admin')
    )
    assert rules(test_user)
    rules = (
        (
            (Rule('username') == 'test')
            & (Rule('age') > 20)
        ) | Rule('roles').contains('admin')
    )
    assert rules(test_user)


def test_multi_conditions_false():
    rules = (
        (
            (Rule('username') == 'test')
            | (Rule('age') > 20)
        ) & Rule('roles').contains('test')
    )
    assert not rules(test_user)
    rules = (
        (Rule('username') == 'test')
        | (Rule('age') > 30)
        | Rule('roles').contains('test')
    )
    assert not rules(test_user)


