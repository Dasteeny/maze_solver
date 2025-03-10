from graphics import Line, Point, Window


def main():
    win = Window(800, 600)
    win.draw_line(line=Line(Point(0, 0), Point(100, 100)), fill_color="red")
    win.wait_for_close()


if __name__ == "__main__":
    main()
