#include <gtk/gtk.h>

// Function prototypes
void on_button_clicked(GtkWidget *widget, gpointer data);
void on_clear_clicked(GtkWidget *widget, gpointer data);

// Main function
int main(int argc, char *argv[]) {
    // Initialize GTK
    gtk_init(&argc, &argv);

    // Create the main window
    GtkWidget *window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(window), "Calculator");
    gtk_container_set_border_width(GTK_CONTAINER(window), 10);
    gtk_widget_set_size_request(window, 200, 250);
    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);

    // Create the grid layout
    GtkWidget *grid = gtk_grid_new();
    gtk_container_add(GTK_CONTAINER(window), grid);

    // Create the entry widget
    GtkWidget *entry = gtk_entry_new();
    gtk_grid_attach(GTK_GRID(grid), entry, 0, 0, 4, 1);

    // Create buttons
    const char *button_labels[] = {
        "7", "8", "9", "/",
        "4", "5", "6", "*",
        "1", "2", "3", "-",
        "0", ".", "=", "+"
    };

    for (int i = 0; i < 16; i++) {
        GtkWidget *button = gtk_button_new_with_label(button_labels[i]);
        gtk_grid_attach(GTK_GRID(grid), button, i % 4, i / 4 + 1, 1, 1);
        g_signal_connect(button, "clicked", G_CALLBACK(on_button_clicked), entry);
    }

    // Create clear button
    GtkWidget *clear_button = gtk_button_new_with_label("Clear");
    gtk_grid_attach(GTK_GRID(grid), clear_button, 0, 5, 4, 1);
    g_signal_connect(clear_button, "clicked", G_CALLBACK(on_clear_clicked), entry);

    // Show all widgets
    gtk_widget_show_all(window);

    // Run the GTK main loop
    gtk_main();

    return 0;
}

// Button click event handler
void on_button_clicked(GtkWidget *widget, gpointer data) {
    const gchar *button_label = gtk_button_get_label(GTK_BUTTON(widget));
    const gchar *entry_text = gtk_entry_get_text(GTK_ENTRY(data));
    gchar *new_entry_text = g_strconcat(entry_text, button_label, NULL);
    gtk_entry_set_text(GTK_ENTRY(data), new_entry_text);
    g_free(new_entry_text);
}

// Clear button click event handler
void on_clear_clicked(GtkWidget *widget, gpointer data) {
    gtk_entry_set_text(GTK_ENTRY(data), "");
}
