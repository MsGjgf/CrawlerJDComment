# _*_ coding : utf-8 _*_
# @Time : 2024/11/6 8:59
# @Author : 哥几个佛
# @File : image
# @Project : CrawlerJDComment

# from flask import Flask, render_template
#
# image_link = ("https://lf-flow-web-cdn.doubao.com/obj/flow-doubao/doubao/web/static/image/logo-icon-white-bg"
#               ".dc28fd5e.png")
#
# app = Flask(__name__, template_folder='templates')
#
#
# def update_image(url: str):
#     global image_link
#     # 这里模拟5秒后图片链接发生变化的情况，实际应用中需要根据真实逻辑来更新这个值
#     image_link = url
#
#
# @app.route('/')
# def show_image():
#     return render_template('image.html', image_url=image_link)
#
#
# @app.route('/check_image_link')
# def check_image_link():
#     return {'new_image_link': image_link}
#
#
# if __name__ == '__main__':
#     app.run(debug=True)

