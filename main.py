##SI507 Final Project##
######tianshu lin######
######tianshul#########


import requests
import networkx as nx
import matplotlib.pyplot as plt
import json
import os


def search_books_by_author(author):
    """
    Search for books written by a given author using the Google Books API.

    Parameters
    ----------
    param1 author : str
        The name of the author to search for.

    Returns
    -------
    list of dict
        A list of dictionaries containing information about the books found. 
        Each dictionary contains the book title and ID.
    """
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
        print(f"The len of the data is available: {len(books)}")
        return books

    except requests.exceptions.HTTPError as HE:
        print(f"An error occurred: {HE}")
        return "Please Enter the valid Author name"
    except Exception as e:
        print(f"Error occurred while searching books by author: {e}")
        return "Please Enter the valid Author name"


def search_books_by_title(title):
    """
    Search for books with a given title using the Google Books API.

    Parameters
    ----------
    param1 title : str
        The title of the book to search for.

    Returns
    -------
    str
        A string of book titles and authors separated by newline characters.
    """
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


def get_book_info(book_id):
    """
    Retrieve information about a book with a given ID using the Google Books API.

    Parameters
    ----------
    param1 book_id : str
        The ID of the book to retrieve information for.

    Returns
    -------
    str
        A string containing the book's title, author(s), and description.
    """
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


def author_network(author):
    """
    Searches the Google Books API for books written by the given author and
    extracts a list of co-authors.
    Parameters
    ----------
    param1 author : str
        The name of the author to search for.

    Returns
    -------
    list
        list of strings representing the names of co-authors of the given
        author. If no co-authors are found, an empty list is returned.
    """
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

        filename = f"{author}_coauthors.json"
        # Check if the file exists and delete it if it does
        if os.path.exists(filename):
            os.remove(filename)
        # Write the JSON data to the file
        with open(filename, 'w') as f:
            json.dump(co_authors, f)
        print(filename)
        return co_authors
    except requests.exceptions.HTTPError as HE:
        print(f'Error occurred during API request: {HE}')
    except requests.exceptions.RequestException as RE:
        print(f'Request exception occurred: {RE}')
    except KeyError as KE:
        print(f'Error occurred during JSON parsing: {KE}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')


def plot_network(author, filename):
    """
    Retrieve information about a book with a given ID using the Google Books API.

    Parameters
    ----------
    param1 author : str
        The name of the author whose co-authors should be plotted.
    param2 filename : str
        The name of the file containing the list of co-authors (in JSON format).
    Returns
    -------
    None
    """
    try:
        with open(filename) as f:
            co_authors = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return

    plt.ion()
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
    plt.pause(5)
    # Disable interactive mode and close the plot
    plt.ioff()
    plt.close()


if __name__ == '__main__':
    while True:
        # Ask the user which task they would like to perform
        task = input("Select a task:\n1. Search books by author\n2. Search books by title\n3. Get book info\n4. See author's co-author network\n5. Exit\n")
        
        if task == '1':
            author = input("Enter an author's name: ")
            books = search_books_by_author(author)
            print(f"Books by {author}:")
            for book in books:
                print(f"{book['title']} ({book['id']})")
            print()

            more_info = input("Do you want more information about a book? (y/n) ")
            if more_info.lower() == 'y':
                book_id = input("Enter a book ID: ")
                print("Searching on website...")
                info = get_book_info(book_id)
                print(info)
                print()

        elif task == '2':
            title = input("Enter a book title: ")
            print("Searching on website...")
            results = search_books_by_title(title)
            print(f"Search results for '{title}':")
            print(results)
            print()

        elif task == '3':
            book_id = input("Enter a book ID: ")
            print("Searching on website...")
            info = get_book_info(book_id)
            print(info)
            print()

        elif task == '4':
            author = input("Enter an author's name: ")
            create_network = input("Do you want to create a network diagram of the author's co-authors? (y/n): ")
            if create_network.lower() == 'y':
                co_authors = author_network(author)
                plot_network(author, filename=f"{author}_coauthors.json")
            else:
                author_network(author=author)
        elif task == '5':
            break
        else:
            print("Invalid input, please try again.")
        
        # Ask the user if they would like to perform another task
        again = input("Would you like to perform another task? (y/n) ")
        if again.lower() != 'y':
            break

