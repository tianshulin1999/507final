import requests
import networkx as nx
import matplotlib.pyplot as plt


def search_books_by_author(author):
    try:
        # Set up the API endpoint URL and search query parameters
        url = 'https://www.googleapis.com/books/v1/volumes'
        params = {'q': f'inauthor:{author}', 'maxResults': 10}

        # Make the API request and store the response
        response = requests.get(url, params=params)

        # Raise an exception if the response status code indicates an error
        response.raise_for_status()

        # Parse the response JSON data and return the book titles and IDs
        data = response.json()
        books = []
        if 'items' not in data:
            print(f"No books found for author '{author}'.")
            return books
        for book in data['items']:
            title = book['volumeInfo']['title']
            book_id = book['id']
            books.append({'title': title, 'id': book_id})
        return books

    except requests.exceptions.HTTPError as HE:
        print(f"An error occurred: {HE}")
        return "Please Enter the valid Author name"
    except Exception as e:
        print(f"Error occurred while searching books by author: {e}")
        return "Please Enter the valid Author name"



# Function to search for books by title
def search_books_by_title(title):
    try:
        # Set up the API endpoint URL and search query parameters
        url = 'https://www.googleapis.com/books/v1/volumes'
        params = {'q': f'intitle:{title}', 'maxResults': 10}

        # Make the API request and store the response
        response = requests.get(url, params=params)

        # Raise an exception if the response status code indicates an error
        response.raise_for_status()

        # Parse the response JSON data and return a string of book titles and authors
        data = response.json()
        books = []
        for book in data['items']:
            title = book['volumeInfo']['title']
            authors = ', '.join(book['volumeInfo']['authors'])
            books.append(f"{title} by {authors}")
        return '\n'.join(books)

    except requests.exceptions.HTTPError as HE:
        print(f"An error occurred: {HE}")
        return "Please Enter the valid book title"

    except Exception as e:
        print(f"Error occurred while searching books by title: {e}")
        return "Please Enter the valid book title"


# Function to get detailed information for a book by ID
def get_book_info(book_id):
    try:
        # Set up the API endpoint URL and make the API request
        url = f'https://www.googleapis.com/books/v1/volumes/{book_id}'
        response = requests.get(url)

        data = response.json()

        if 'volumeInfo' in data:
            title = data['volumeInfo'].get('title', 'Title not available')
            authors = ', '.join(data['volumeInfo'].get('authors', ['Unknown']))
            description = data['volumeInfo'].get('description', 'Description not available')
            return f"{title} by {authors}\n\n{description}"
        else:
            return 'Book information not available'
    except Exception as e:
        print(f"Error occurred while getting book information: {e}")
        return "Please Enter the valid Book ID"


# Function to create a network diagram of an author's co-authors
def author_network(author):
    try:
        # Set up the API endpoint URL and search query parameters
        url = 'https://www.googleapis.com/books/v1/volumes'
        params = {'q': f'inauthor:{author}', 'maxResults': 10}

        # Make the API request and store the response
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception if response status code indicates an error

        # Parse the response JSON data and extract the author's co-authors
        data = response.json()
        co_authors = []
        for book in data['items']:
            if 'authors' in book['volumeInfo']:
                co_authors += book['volumeInfo']['authors']
        co_authors = list(set(co_authors))  # Remove duplicates

        # Create a network graph of the co-authors
        G = nx.Graph()
        G.add_node(author)
        for co_author in co_authors:
            G.add_node(co_author)
            G.add_edge(author, co_author)

        # Plot the network graph
        pos = nx.spring_layout(G)
        plt.figure(figsize=(10, 10))
        nx.draw_networkx_nodes(G, pos, node_color='r', node_size=500, alpha=0.8)
        nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
        plt.axis('off')
        plt.show()
        plt.savefig("Author_Co Author network.png")

    except requests.exceptions.HTTPError as HE:
        print(f'Error occurred during API request: {HE}')
    except requests.exceptions.RequestException as RE:
        print(f'Request exception occurred: {RE}')
    except KeyError as KE:
        print(f'Error occurred during JSON parsing: {KE}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

user_input = input('Do you want to search by author or by book title? Please answer either author or title:')
if __name__ == '__main__':
    if user_input == 'author':
        author = input("Enter an author's name: ")
        books = search_books_by_author(author)
        print(f"Books by {author}:")
        for book in books:
            print(f"{book['title']} ({book['id']})")
        print()
    if user_input == 'title':
        title = input("Enter a book title: ")
        print("Searching on website...")
        results = search_books_by_title(title)
        print(f"Search results for '{title}':")
        print(results)
        print() 
    else: 
        print("please enter only 'author' or 'title' to speific your searching")





""" if __name__ == '__main__':
    # Call the search_books_by_author() function and print the results
    author = input("Enter an author's name: ")
    books = search_books_by_author(author)
    print(f"Books by {author}:")
    for book in books:
        print(f"{book['title']} ({book['id']})")
    print()

    # Call the search_books_by_title() function and print the results
    title = input("Enter a book title: ")
    print("Searching on website...")
    results = search_books_by_title(title)
    print(f"Search results for '{title}':")
    print(results)
    print() 
 """


""" if __name__ == '__main__':
    # Call the search_books_by_author() function and print the results
    author = input("Enter an author's name: ")
    books = search_books_by_author(author)
    print(f"Books by {author}:")
    for book in books:
        print(f"{book['title']} ({book['id']})")
    print()

    # Call the search_books_by_title() function and print the results
    title = input("Enter a book title: ")
    print("Searching on website...")
    results = search_books_by_title(title)
    print(f"Search results for '{title}':")
    print(results)
    print() """ """

    # Call the get_book_info() function and print the results. 
    book_id = input("Enter a book ID: ")
    print("Searching on website...")
    info = get_book_info(book_id)
    print(info)
    print()

    # Call the author_network() function
    author = input("Enter an author's name to see their co-author network: ")
    print("Searching on website...")
    author_network(author)

 """