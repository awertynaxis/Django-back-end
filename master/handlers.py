import uuid
from master.models import VerifyCodes


def generate_code(master):
    # TODO: docstring
    code = str(uuid.uuid4())
    set_code(master, code)


def set_code(master, code):
    # TODO: docstring
    query_object = VerifyCodes(master=master, code=code)
    query_object.save()


def get_user_id_if_approve(query_data):
    """Returns user_id if verify_code received from Telegram matches verify_code in database."""
    verify_code = query_data['verify_code']
    # TODO: describe what's going on on the next line, just in case
    master_id = VerifyCodes.objects.filter(code=verify_code).values('master').distinct()[0].get('master')
    return master_id




