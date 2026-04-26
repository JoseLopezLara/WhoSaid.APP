import os
import json

class StorageManager:
    """Clase encargada de gestionar la creación de carpetas y persistencia de resultados."""
    
    def __init__(self, base_dir="processed_files"):
        self.base_dir = base_dir

    def setup_directories(self):
        """Crea la estructura inicial de directorios."""
        directories = [
            self.base_dir,
            os.path.join(self.base_dir, "processed_transcriptions"),
            os.path.join(self.base_dir, "processed_n_gramas", "creators"),
            os.path.join(self.base_dir, "processed_n_gramas", "global", "first_appearance"),
            os.path.join(self.base_dir, "processed_n_gramas", "global", "all_appearances")
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def save_results(self, top_results, analyzer):
        """Guarda los resultados finales en la estructura de archivos."""
        if not top_results:
            return

        global_union_first = {}
        global_union_all = {}
        global_interception_first = {}
        global_interception_all = {}

        for creator, results in top_results.items():
            # Formatear datos
            union_first = analyzer.format_results(results['union'], 'first_appearance')
            union_all = analyzer.format_results(results['union'], 'all_appearances')
            interception_first = analyzer.format_results(results['intersection'], 'first_appearance')
            interception_all = analyzer.format_results(results['intersection'], 'all_appearances')

            # Acumular para global
            global_union_first[creator] = union_first
            global_union_all[creator] = union_all
            global_interception_first[creator] = interception_first
            global_interception_all[creator] = interception_all

            # Carpetas del creador
            creator_dir = os.path.join(self.base_dir, "processed_n_gramas", "creators", creator)
            for mode in ["first_appearance", "all_appearances"]:
                os.makedirs(os.path.join(creator_dir, mode), exist_ok=True)

            # Guardar archivos del creador
            self._write_json(os.path.join(creator_dir, "first_appearance", "n_gramas_union.json"), union_first)
            self._write_json(os.path.join(creator_dir, "first_appearance", "n_gramas_interception.json"), interception_first)
            self._write_json(os.path.join(creator_dir, "all_appearances", "n_gramas_union.json"), union_all)
            self._write_json(os.path.join(creator_dir, "all_appearances", "n_gramas_interception.json"), interception_all)

            print(f"Saved results for creator: {creator}")

        # Guardar archivos globales
        global_path = os.path.join(self.base_dir, "processed_n_gramas", "global")
        self._write_json(os.path.join(global_path, "first_appearance", "n_gramas_union.json"), global_union_first)
        self._write_json(os.path.join(global_path, "first_appearance", "n_gramas_interception.json"), global_interception_first)
        self._write_json(os.path.join(global_path, "all_appearances", "n_gramas_union.json"), global_union_all)
        self._write_json(os.path.join(global_path, "all_appearances", "n_gramas_interception.json"), global_interception_all)

        print("\nAll global results successfully generated and saved.")

    def _write_json(self, file_path, data):
        """Método auxiliar para escribir JSON."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
