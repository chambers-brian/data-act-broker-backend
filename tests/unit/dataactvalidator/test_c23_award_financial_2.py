from random import randint, choice
from string import ascii_uppercase, ascii_lowercase, digits
from tests.unit.dataactcore.factories.staging import AwardFinancialFactory, AwardProcurementFactory
from tests.unit.dataactvalidator.utils import number_of_errors, query_columns

_FILE = 'c23_award_financial_2'

def test_column_headers(database):
    expected_subset = {"row_number", "transaction_obligated_amou_sum", "federal_action_obligation_sum"}
    actual = set(query_columns(_FILE, database))
    assert expected_subset <= actual

def test_success(database):
    """ Test that a four digit object class with no flag is a success, and a three digit object class with a flag is a success"""
    # Create a 12 character random parent_award_id
    parent_award_id = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for i in range(12))
    parent_award_id_two = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for i in range(12))
    first_parent_award_id_row_one = AwardFinancialFactory(object_class = randint(1100,1999),
        by_direct_reimbursable_fun = "d", transaction_obligated_amou = 1234, parent_award_id = parent_award_id)
    first_parent_award_id_row_two = AwardFinancialFactory(object_class = randint(1000,1099),
        by_direct_reimbursable_fun = "d", transaction_obligated_amou = 2345, parent_award_id = parent_award_id)
    # And add a row for a different parent_award_id
    second_parent_award_id_row_one = AwardFinancialFactory(object_class = randint(1100,1999),
        by_direct_reimbursable_fun = "d", transaction_obligated_amou = 9999, parent_award_id = parent_award_id_two)
    first_ap_row = AwardProcurementFactory(parent_award_id = parent_award_id, federal_action_obligation = -2468)
    second_ap_row = AwardProcurementFactory(parent_award_id = parent_award_id, federal_action_obligation = -1100)
    third_ap_row = AwardProcurementFactory(parent_award_id = parent_award_id, federal_action_obligation = -11)
    other_parent_award_id_ap_row = AwardProcurementFactory(parent_award_id = parent_award_id_two, federal_action_obligation = -9999)

    errors = number_of_errors(_FILE, database, models=[first_parent_award_id_row_one, first_parent_award_id_row_two, second_parent_award_id_row_one, first_ap_row, second_ap_row, third_ap_row, other_parent_award_id_ap_row])
    assert errors == 0


def test_failure(database):
    """ Test that a three digit object class with no flag is an error"""
    # Create a 12 character random parent_award_id
    parent_award_id = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for i in range(12))
    parent_award_id_two = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for i in range(12))
    first_parent_award_id_row_one = AwardFinancialFactory(object_class = randint(1100,1999),
        by_direct_reimbursable_fun = "d", transaction_obligated_amou = 1234, parent_award_id = parent_award_id)
    first_parent_award_id_row_two = AwardFinancialFactory(object_class = randint(1000,1099),
        by_direct_reimbursable_fun = "d", transaction_obligated_amou = 2345, parent_award_id = parent_award_id)
    # And add a row that shouldn't be included
    second_parent_award_id_row_one = AwardFinancialFactory(object_class = randint(1100,1999),
        by_direct_reimbursable_fun = "d", transaction_obligated_amou = 9999, parent_award_id = parent_award_id_two)
    first_ap_row = AwardProcurementFactory(parent_award_id = parent_award_id, federal_action_obligation = -2468)
    second_ap_row = AwardProcurementFactory(parent_award_id = parent_award_id, federal_action_obligation = -1000)
    other_parent_award_id_ap_row = AwardProcurementFactory(parent_award_id = parent_award_id_two, federal_action_obligation = -1111)

    errors = number_of_errors(_FILE, database, models=[first_parent_award_id_row_one, first_parent_award_id_row_two, second_parent_award_id_row_one, first_ap_row, second_ap_row, other_parent_award_id_ap_row])
    assert errors == 2