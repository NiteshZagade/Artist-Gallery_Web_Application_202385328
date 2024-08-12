from werkzeug.serving import run_simple
import multiprocessing

BASE_URL = "127.0.0.1"

def run_user_service():
    from user_service.app import app as user_app
    run_simple(BASE_URL, 5001, user_app)

def run_product_service():
    from product_service.app import app as product_app
    run_simple(BASE_URL, 5002, product_app)
    
def run_order_service():
    from order_service.app import app as order_app
    run_simple(BASE_URL, 5003, order_app)

def run_payment_service():
    from payment_service.app import app as payment_app
    run_simple(BASE_URL, 5004, payment_app)

if __name__ == "__main__":
    user_process = multiprocessing.Process(target=run_user_service)
    product_process = multiprocessing.Process(target=run_product_service)
    order_process = multiprocessing.Process(target=run_order_service)
    payment_process = multiprocessing.Process(target=run_payment_service)

    user_process.start()
    product_process.start()
    order_process.start()
    payment_process.start()

    user_process.join()
    product_process.join()
    order_process.join()
    payment_process.join()
