from tests.crud.AnyTestBusinessObject import BUSINESS_OBJECT_NAME as TEST_BO
from tests.crud.RelatedTestBusinessObject import BUSINESS_OBJECT_NAME as RELATED_TEST_BO

data = {
    TEST_BO: [
        {
            "id": 1234,
            "strfield": "1234",
            "intfield": 1234
        },
        {
            "id": 9876,
            "strfield": "9876",
            "intfield": 9876,
            "foreign_field": 1234  # Relates to RELATED_TEST_BO with id == 1234
        }
    ],
    RELATED_TEST_BO: [
        {
            "id": 1234,
            "strfield": "1234"
        }
    ]
}
