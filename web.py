from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>开歌辅助</title>
</head>
<body>
      <h1>开歌辅助</h1>
      <form id="searchForm">
          <label for="wordCount">你所要开的歌的字数呢~：</label>
          <input type="number" id="wordCount" name="wordCount">
          <button type="button" onclick="addQuestions()">喵</button>
          <div id="questions"></div>
          <button type="submit" id="submitBtn">搜索</button>
      </form>
      <div id="result"></div>

      <script>
          function addQuestions() {
              var wordCount = document.getElementById('wordCount').value;
              var questionsDiv = document.getElementById('questions');
              questionsDiv.innerHTML = '';

              for (var i = 1; i <= wordCount; i++) {
                  var questionLabel = document.createElement('label');
                  questionLabel.innerText = '你知道的第' + i + '项的字母是什么呢喵~？';
                  var questionInput = document.createElement('input');
                  questionInput.type = 'text';
                  questionInput.name = 'char' + i;
                  questionsDiv.appendChild(questionLabel);
                  questionsDiv.appendChild(questionInput);
                  questionsDiv.appendChild(document.createElement('br'));
              }
          }

          document.getElementById('searchForm').onsubmit = function(event) {
              event.preventDefault();
              var formData = new FormData(this);
              var data = {};
              formData.forEach((value, key) => data[key] = value);
              fetch('/search', {
                  method: 'POST',
                  body: JSON.stringify(data),
                  headers: {
                      'Content-Type': 'application/json',
                  },
              })
              .then(response => response.json())
              .then(data => {
                  document.getElementById('result').innerText = data.message;
              })
              .catch(error => {
                  console.error('Error:', error);
              });
          };
      </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.json
        word_count = int(data['wordCount'])
        known_chars = [data.get(f'char{i}') for i in range(1, word_count + 1)]
        found_lines = []

        with open('songs.txt', 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                if len(line.strip()) == word_count:
                    match = True
                    for i, char in enumerate(line.strip()):
                        if known_chars[i] and char.lower() != known_chars[i].lower():
                            match = False
                            break
                    if match:
                        found_lines.append(line.strip())

        if found_lines:
            result_message = "找到了呢~：\n" + "\n".join(found_lines)
        else:
            result_message = "没有找到匹配的歌曲喵~。"

        return jsonify({'message': result_message})
    except Exception as e:
        return jsonify({'message': f"发生错误：{e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)