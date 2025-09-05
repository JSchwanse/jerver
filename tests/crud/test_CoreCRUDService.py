import unittest

from sqlalchemy.exc import NoResultFound, DataError

from jerver.inject import useInject
from jester.Assertions import Assertions
from jester.DatabaseTestCases import DatabaseTestCases
from tests.crud.AnyTestBusinessObject import AnyTestBusinessObject
from tests.crud.AnyTestBusinessObjectCRUDService import AnyTestBusinessObjectCRUDService


class CoreCRUDServiceTest(DatabaseTestCases.BaseDatabaseTest):
    test_bo_service: AnyTestBusinessObjectCRUDService = useInject(AnyTestBusinessObjectCRUDService)

    def test_get_call(self):
        test_bo_id = 1234
        test_bo: AnyTestBusinessObject = self.test_bo_service.get(test_bo_id)

        self.assertIsNotNone(test_bo)
        self.assertEqual(test_bo_id, test_bo.id)

    def test_find_call(self):
        # Test case for matching results
        test_filter = {
            'strfield': '9876'
        }
        bo_list: list[AnyTestBusinessObject] = self.test_bo_service.find(test_filter)

        self.assertIsNotNone(bo_list)
        self.assertEqual(2, len(bo_list))
        Assertions.assertAnyInList(bo_list, lambda x: x.id == 9876)
        Assertions.assertAnyInList(bo_list, lambda x: x.id == 5555)
        Assertions.assertAllInList(bo_list, lambda x: x.strfield == '9876')
        Assertions.assertAnyInList(bo_list, lambda x: x.foreign_field == 1234)
        test_bo = bo_list[1]
        self.assertIsNotNone(test_bo.foreign_object)
        self.assertEqual(1234, test_bo.foreign_object.id)
        self.assertEqual('1234', test_bo.foreign_object.strfield)

        # Test case for empty result set
        empty_filter = {
            'strfield': 'nonexistent'
        }
        empty_list = self.test_bo_service.find(empty_filter)
        self.assertEqual(0, len(empty_list))

    def test_save_call_for_create(self):
        test_id = 852

        # make sure object does not exist, yet
        test_bo_list = self.test_bo_service.find({'id': test_id})
        self.assertIsNotNone(test_bo_list)
        self.assertTrue(isinstance(test_bo_list, list))
        self.assertEqual(0, len(test_bo_list))

        # create and save object
        test_bo = AnyTestBusinessObject(id=test_id, strfield='852', intfield=852)
        saved_test_bo = self.test_bo_service.save(test_bo)

        self.assertIsNotNone(saved_test_bo)

        # opposite check: load from db
        loaded_bo = self.test_bo_service.get(saved_test_bo.id)
        self.assertIsNotNone(loaded_bo)
        self.assertEqual(852, loaded_bo.id)
        self.assertEqual('852', loaded_bo.strfield)
        self.assertEqual(852, loaded_bo.intfield)

    def test_save_call_for_update(self):
        test_id = 9876

        # make sure object does exist already
        test_bo_list: list[AnyTestBusinessObject] = self.test_bo_service.find({'id': test_id})
        self.assertIsNotNone(test_bo_list)
        self.assertTrue(isinstance(test_bo_list, list))
        self.assertEqual(1, len(test_bo_list))

        test_bo = test_bo_list[0]
        self.assertEqual(test_id, test_bo.id)
        self.assertEqual(9876, test_bo.intfield)
        self.assertEqual('9876', test_bo.strfield)

        # change the bo and save the changes
        test_bo.intfield = 999999
        test_bo.strfield = 'anyString'

        saved_bo = self.test_bo_service.save(test_bo)
        self.assertEqual(test_id, saved_bo.id)
        self.assertEqual(999999, saved_bo.intfield)
        self.assertEqual('anyString', saved_bo.strfield)

        # load the bo again from db and check values, use find to clarify that there's still only one object
        loaded_bo_list: list[AnyTestBusinessObject] = self.test_bo_service.find({'id': test_id})
        self.assertIsNotNone(loaded_bo_list)
        self.assertTrue(isinstance(loaded_bo_list, list))
        self.assertEqual(1, len(loaded_bo_list))  # => still 1, ensures no new object was created

        loaded_bo = loaded_bo_list[0]
        self.assertEqual(test_id, loaded_bo.id)
        self.assertEqual(999999, loaded_bo.intfield)
        self.assertEqual('anyString', loaded_bo.strfield)

    def test_delete_call(self):
        test_id = 1234

        # ensure bo exists
        test_bo: AnyTestBusinessObject = self.test_bo_service.get(test_id)
        self.assertIsNotNone(test_bo)

        # delete bo
        is_deleted = self.test_bo_service.delete(test_bo)
        self.assertTrue(is_deleted)

        # check if it's deleted
        with self.assertRaises(NoResultFound) as assertion_result:
            test_bo: AnyTestBusinessObject = self.test_bo_service.get(test_id)

        self.assertEqual('No row was found when one was required', assertion_result.exception.args[0])

    def test_error_on_get_call(self):
        test_bo_id = 9999  # => does not exist

        with self.assertRaises(NoResultFound) as assertion_result:
            test_bo: AnyTestBusinessObject = self.test_bo_service.get(test_bo_id)

        self.assertEqual('No row was found when one was required', assertion_result.exception.args[0])

    def test_error_on_save_call(self):
        test_bo_id = 1234

        test_bo: AnyTestBusinessObject = self.test_bo_service.get(test_bo_id)

        test_bo.intfield = 'Not an int'  # set str value to int field to provoke an error on save

        with self.assertRaises(DataError) as assertion_result:
            # saving the object should cause an error
            test_bo = self.test_bo_service.save(test_bo)


if __name__ == '__main__':
    unittest.main()
