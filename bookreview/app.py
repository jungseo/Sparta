from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/review', methods=['POST'])
def write_review():
    # 1. 클라이언트가 준 title, author, review 가져오기.
    # title_receive로 클라이언트가 준 title 가져오기
    title_receive = request.form['title_give']

    # author_receive로 클라이언트가 준 author 가져오기
    author_receive = request.form['author_give']
    # review_receive로 클라이언트가 준 review 가져오기
    review_receive = request.form['review_give']

    # 2. DB에 정보 삽입하기
    review = {
        'title': title_receive,
        'author': author_receive,
        'review': review_receive
    }
    db.reviews.insert_one(review)
    print('[서버알림] 성공적으로 DB 에 저장했습니다')
    print('[서버알림] write_Review 가 클라이언트의 요청을 성공적으로 수행했습니다')
    # 3. 성공 여부 & 성공 메시지 반환하기
    return jsonify({'result': 'success', 'msg': '이 요청은 POST!'})


@app.route('/review', methods=['GET'])
def read_reviews():
    reviews = list(db.reviews.find({}, {'_id': 0}))
    print('[서버 알림]')
    print(reviews)

    return jsonify({'result': 'success', 'reviews': reviews})


if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)
