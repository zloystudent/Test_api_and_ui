import allure
from random import randint

class DataGenerator:
    @staticmethod
    @allure.step("Generate random post code")
    def generate_random_post_code() -> str:
        post_code = "".join([f"{randint(0, 9)}" for _ in range(10)])
        allure.attach(post_code, name="Generated Post Code", attachment_type=allure.attachment_type.TEXT)
        return post_code
    
    @staticmethod
    @allure.step("Generate name from post code: {post_code}")
    def generate_name_from_post_code(post_code: str) -> str:
        random_post_code = int(post_code)
        mirror_random_name = ""
        
        while random_post_code != 0:
            generate_symbol = chr(((random_post_code % 100) % 26) + 97)
            random_post_code = random_post_code // 100
            mirror_random_name = mirror_random_name + generate_symbol
            
        name = mirror_random_name[::-1]
        allure.attach(name, name="Generated Name", attachment_type=allure.attachment_type.TEXT)
        return name