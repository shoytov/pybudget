from src.resources.down import DownResources
from src.resources.up import InitResources
from src.ui.ui_app import BudgetApp


def main():
    try:
        InitResources()
        app = BudgetApp()
        app.run()
    finally:
        DownResources()


if __name__ == "__main__":
    main()
