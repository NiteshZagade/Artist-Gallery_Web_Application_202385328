from datetime import datetime
from enum import Enum

def format_datetime(dt):
    if not dt:
        return None
    return dt.strftime('%d-%b-%Y %H:%M')

def format_datetime(dt, fmt='%Y-%m-%d %H:%M:%S'):
        if isinstance(dt, datetime):
            return dt.strftime(fmt)
        return dt
    
@staticmethod
def get_enum_value(enum_class: Enum, enum_string: str, default=0):
    """
    Generic method to get the value of an enum member by its name.

    :param enum_class: The enum class to search in.
    :param enum_string: The name of the enum member as a string.
    :param default: The default value to return if no match is found.
    :return: The value of the enum member if found, else the default value.
    """
    for enum_member in enum_class:
        if enum_member.name == enum_string:
            return enum_member.value
    return default

def get_value_from_label(enum_class, label, default=0):
    reverse_map = enum_class.reverse_mapping()
    for key, value in reverse_map.items():
        if value.lower() == label.lower():
            return key
    return default

def generate_unique_id(last_used_id, identifier):
    num = 1000
    if last_used_id:
        last_id = last_used_id.id
    else:
        last_id = 0
    next_id = num + last_id + 1
    alphanumeric_id = identifier + str(next_id)
    return alphanumeric_id

def generate_unique_product_id(last_product, today, identifier):    
    if last_product:
        # Extract the batch and sequential number from the last product ID
        last_batch = int(last_product.product_id[4:7])
        last_date = last_product.product_id[8:14]
        last_seq = int(last_product.product_id[15:])
    else:
        last_batch = 1
        last_date = today
        last_seq = 0
    
    # Reset sequence number if the date has changed
    if last_date != today:
        last_seq = 0

    # Increment the sequence number
    next_seq = last_seq + 1

    # Increment the batch number if the sequence reaches 9999
    if next_seq > 9999:
        last_batch += 1
        next_seq = 1

    # Format the new product ID
    product_id = f"{identifier}-{str(last_batch).zfill(3)}-{today}-{str(next_seq).zfill(4)}"
    
    return product_id