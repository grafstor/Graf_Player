from tkinter.filedialog import askdirectory

class File_Manager:

    def get_path(self):
        try:
            path = self.read_path()
            if not path:
                path = self.ask_dir()
                return path
            return path
        except:
            path = self.ask_dir()
            return path

    def ask_dir(self):
        path = askdirectory(initialdir="C:/Users/",
                            title = "Choose a folder with music")
        self.write_path(path)
        return path

    def write_path(self, path):
        dirr = open("bd.txt","w")
        dirr.write(path)
        dirr.close()

    def read_path(self):
        dirr = open("bd.txt","r")
        path = dirr.read()
        dirr.close()
        return path.strip()