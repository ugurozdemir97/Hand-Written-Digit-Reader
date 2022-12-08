from tkinter import *
import numpy as np
from PIL import ImageGrab, ImageOps, Image
import os

NETWORK = True


# ------------------------------------ BACK PROP --------------------------------------- #

def update_params(w1, b1, w2, b2, dw1, db1, dw2, db2, alpha):
    w1 = w1 - alpha * dw1
    b1 = b1 - alpha * db1
    w2 = w2 - alpha * dw2
    b2 = b2 - alpha * db2
    return w1, b1, w2, b2


def deriv_ReLU(Z):
    return Z > 0


def one_hot(y):
    one_hot_Y = np.zeros((y.size, 10))
    one_hot_Y[np.arange(y.size), y] = 1
    one_hot_Y = one_hot_Y.T
    return one_hot_Y


def back_prop(Z1, A1, A2, w2, x, y):
    one_hot_Y = one_hot(y)
    dZ2 = A2 - one_hot_Y
    dw2 = 1 / 1 * dZ2.dot(A1.T)
    db2 = 1 / 1 * np.sum(dZ2)

    dZ1 = w2.T.dot(dZ2) * deriv_ReLU(Z1)
    dw1 = 1 / 1 * dZ1.dot(x.T)
    db1 = 1 / 1 * np.sum(dZ1)
    return dw1, db1, dw2, db2


# ------------------------------------ FORWARD PROP --------------------------------------- #

def ReLU(Z):
    return np.maximum(Z, 0)


def softmax(Z):
    A = np.exp(Z) / sum(np.exp(Z))
    return A


def forward_prop(w_input, b_input, w_hidden, b_hidden, test):
    Z1 = w_input.dot(test) + b_input
    A1 = ReLU(Z1)
    Z2 = w_hidden.dot(A1) + b_hidden
    A2 = softmax(Z2)
    return Z1, A1, Z2, A2


def get_predictions(A2):
    return np.argmax(A2, 0)


def make_predictions(test, w_input, b_input, w_hidden, b_hidden):
    Z1, A1, Z2, A2 = forward_prop(w_input, b_input, w_hidden, b_hidden, test)
    if entry.get() != "":  # If you typed the answer in entry, it will be used to train Neural Network by sending it
        # to back-prop, overtime the network will get better and better finding the true answer.
        answer = np.array(int(entry.get()))
        dw1, db1, dw2, db2 = back_prop(Z1, A1, A2, w_hidden, test, answer)
        w_input, b_input, w_hidden, b_hidden = update_params(w_input, b_input, w_hidden, b_hidden,
                                                             dw1, db1, dw2, db2, 0.005)
        np.save("Data/Input Weight.npy", w_input)  # Save the new weights and bias.
        np.save("Data/Hidden Weight.npy", w_hidden)
        np.save("Data/Input Bias.npy", b_input)
        np.save("Data/Hidden Bias.npy", b_hidden)
        entry.delete(0, END)
        rectangles = canvas.find_all()
        for g in rectangles:
            canvas.delete(g)
    predictions = get_predictions(A2)
    return predictions


# ------------------------------------ PROGRAM FUNCTIONS --------------------------------------- #

def send():
    image = ImageGrab.grab(bbox=(
        canvas.winfo_rootx() + 130,
        canvas.winfo_rooty() + 60,
        canvas.winfo_rootx() + 130 + canvas.winfo_width() + 130,
        canvas.winfo_rooty() + 60 + canvas.winfo_height() + 130))
    image = image.resize((28, 28))
    image = ImageOps.grayscale(image)
    image.save("Temporary.png")  # Temporarily save the image as png to convert it into numpy arrays

    image = Image.open("Temporary.png")

    img = np.asarray(image) / 255  # We divide to 255 so all pixel values will be between 1 and 0.
    test = img.reshape(784, 1)

    try:
        weight_input = np.load("Data/Input Weight.npy")
        weight_hidden = np.load("Data/Hidden Weight.npy")
        bias_input = np.load("Data/Input Bias.npy")
        bias_hidden = np.load("Data/Hidden Bias.npy")
    except FileNotFoundError:  # Show error if files cannot be found.
        rectangles = canvas.find_all()
        for g in rectangles:
            canvas.delete(g)
        canvas.create_text(280, 260, text="Neural Network Does Not Found", font=("Arial", 20, "bold"), fill="white")
        send.config(command=NONE)
        cancel.config(command=NONE)
        window.unbind("<B1-Motion>")
    else:
        prediction = make_predictions(test, weight_input, bias_input, weight_hidden, bias_hidden)
        label.config(text=f"Prediction: {prediction}")


# ------------------------------ DELETE DRAWING ---------------------------- #

def cancel():
    label.config(text="Prediction: [ ]")
    entry.delete(0, END)

    rectangles = canvas.find_all()  # Find everything on canvas
    for g in rectangles:
        canvas.delete(g)


def paint(event):  # Draw line from the old position to new position of cursor.
    x = event.x
    y = event.y
    canvas.create_line(x, y, event.x, event.y, fill="white", width=33, capstyle=ROUND, smooth=TRUE, splinesteps=10)


def quits():  # Delete the temporary image file after quit.
    window.quit()
    if os.path.exists("Temporary.png"):
        os.remove("Temporary.png")


# ----------------------------------------------- WINDOW SETUP ------------------------------------------------------ #

window = Tk()
window.title("Hand Written Digit Reader")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_cordinate = int((screen_width / 2) - (600 / 2))
y_cordinate = int((screen_height / 2) - (600 / 2))

window.geometry("{}x{}+{}+{}".format(600, 600, x_cordinate, y_cordinate))
window.config(pady=20, padx=20, bg="white")

package = Frame(bg="white")
package.pack(expand=True)

frame = Frame(package, bg="white")
frame.pack(side=TOP, expand=True, fill=X, anchor=NW)

send = Button(frame, text="SEND", padx=20, pady=8, bg="gold", command=send)
cancel = Button(frame, text="CANCEL", padx=20, pady=8, bg="red", fg="white", command=cancel)
label = Label(frame, text="Prediction: [ ]", font=("Arial", 13, "bold"), bg="white")
teach = Label(frame, text="Teach: ", font=("Arial", 13, "bold"), bg="white")
entry = Entry(frame, width=5, font=13)

label.pack(side=RIGHT, padx=20)
entry.pack(side=RIGHT, padx=(5, 20))
teach.pack(side=RIGHT)
send.pack(side=LEFT, padx=1)
cancel.pack(side=LEFT, padx=1)

canvas = Canvas(package)
canvas.config(width=560, height=560, bg="black")
canvas.pack(expand=True)

window.bind("<B1-Motion>", paint)
window.protocol('WM_DELETE_WINDOW', quits)  # For deleting the temporary files after closing the window.

window.mainloop()
