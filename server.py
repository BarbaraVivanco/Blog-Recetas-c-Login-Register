from login_register import app

from login_register.controllers import log_regs, recipes

if __name__=="__main__":
    app.run(debug=True)