from cite_categorizer.categorizer import CiteCategorizer

def main():
    palabra = input("Enter the keyword (palabra): ").strip().lower().replace(" ", "_")
    categorizer = CiteCategorizer(palabra)
    categorizer.run()

if __name__ == "__main__":
    main()
