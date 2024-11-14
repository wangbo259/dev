# 我的第一次尝试
这个真的好用吗

# 如果我输入代码呢
```python{number}
# 这是一个带有行号的Python代码块
print("Hello, World!")
```
```
mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0
```