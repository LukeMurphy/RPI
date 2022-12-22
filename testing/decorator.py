def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        print(func(3))
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_whee(n):
    print("Whee!")
    return 2.0 * n


say_whee()
