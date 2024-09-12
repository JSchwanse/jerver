import unittest

from jerver.inject import useInject
from jester.Assertions import Assertions
from jester.DatabaseTestCases import DatabaseTestCases
from tests.crud.AnyTestBusinessObject import AnyTestBusinessObject
from tests.crud.AnyTestBusinessObjectCRUDService import AnyTestBusinessObjectCRUDService


class CoreCRUDServiceTest(DatabaseTestCases.BaseDatabaseTest):
    test_bo_service = useInject(AnyTestBusinessObjectCRUDService)

    def test_get_call(self):
        test_bo_id = 1234
        test_bo: AnyTestBusinessObject = self.test_bo_service.get(test_bo_id)

        self.assertIsNotNone(test_bo)
        self.assertEqual(test_bo_id, test_bo.id)

    def test_find_call(self):
        test_filter = {
            'strfield': '9876'
        }
        bo_list: list[AnyTestBusinessObject] = self.test_bo_service.find(test_filter)

        self.assertIsNotNone(bo_list)
        self.assertEqual(1, len(bo_list))
        Assertions.assertAnyInList(bo_list, lambda x: x.id == 9876)
        Assertions.assertAllinList(bo_list, lambda x: x.strfield == '9876')
        Assertions.assertAllinList(bo_list, lambda x: x.foreign_field == 1234)
        test_bo = bo_list[0]
        self.assertIsNotNone(test_bo.foreign_object)
        self.assertEqual(1234, test_bo.foreign_object.id)
        self.assertEqual('1234', test_bo.foreign_object.strfield)

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
        pass

    def test_delete_call(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
