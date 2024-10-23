#include <QtWidgets>

class Calculator : public QWidget {
    Q_OBJECT
public:
    Calculator(QWidget *parent = 0) : QWidget(parent) {
        // Set up the layout
        QGridLayout *layout = new QGridLayout(this);
        display = new QLineEdit();
        display->setAlignment(Qt::AlignRight);
        display->setReadOnly(true);
        layout->addWidget(display, 0, 0, 1, 4);

        // Create buttons
        const char *buttons[16] = {
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        };

        for (int i = 0; i < 16; ++i) {
            QPushButton *button = createButton(buttons[i]);
            layout->addWidget(button, i / 4 + 1, i % 4);
        }

        // Connect signals and slots
        connect(qApp, SIGNAL(focusChanged(QWidget*,QWidget*)), this, SLOT(onFocusChanged()));
        connect(display, SIGNAL(textChanged(const QString&)), this, SLOT(onTextChanged(const QString&)));
    }

private slots:
    void onFocusChanged() {
        if (qApp->focusWidget() != display) {
            display->clearFocus();
        }
    }

    void onTextChanged(const QString &text) {
        Q_UNUSED(text);
        display->setCursorPosition(display->text().length());
    }

    void onButtonClicked() {
        QPushButton *button = qobject_cast<QPushButton *>(sender());
        if (button) {
            const QString &text = button->text();
            if (text == "=") {
                evaluate();
            } else if (text == "C") {
                display->clear();
            } else {
                display->insert(text);
            }
        }
    }

private:
    void evaluate() {
        QString expression = display->text();
        QScriptEngine engine;
        QScriptValue result = engine.evaluate(expression);
        if (result.isValid()) {
            display->setText(result.toString());
        } else {
            display->setText("Error");
        }
    }

    QPushButton *createButton(const QString &text) {
        QPushButton *button = new QPushButton(text);
        connect(button, SIGNAL(clicked()), this, SLOT(onButtonClicked()));
        return button;
    }

    QLineEdit *display;
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    Calculator calc;
    calc.setWindowTitle("Calculator");
    calc.show();
    return app.exec();
}

#include "main.moc"
