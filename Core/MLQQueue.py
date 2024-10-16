from typing import Optional
from Core.Process import Process
from queue import PriorityQueue

class MLQQueue:
    """
    Clase que representa una cola en el algoritmo MLQ (Multi-Level Queue), con soporte para diferentes políticas de planificación.

    Atributos:
    ----------
    name : str
        Nombre de la cola, que puede indicar su política de planificación (e.g., "RR1" para Round Robin con quantum 1, "SJF" para Shortest Job First).
    
    quantum : Optional[int]
        Valor del quantum para las colas que usan Round Robin (RR). Si es None, indica que la cola no utiliza quantum (como en el caso de SJF).
    
    processes : PriorityQueue
        Cola de prioridad para gestionar los procesos. La prioridad de los procesos en la cola está determinada por `last_execution_time`, que indica el último momento en que fueron ejecutados.
    """
    def __init__(self, name: str, quantum: Optional[int] = None):
        """
        Inicializa una cola MLQ con un nombre y, opcionalmente, un quantum.

        Parámetros:
        -----------
        name : str
            El nombre de la cola que identifica la política de planificación que sigue.
        
        quantum : Optional[int]
            Si es proporcionado, este valor de quantum se usará para la planificación Round Robin.
            Si es None, la cola funcionará con otra política (e.g., SJF).
        """
        self.name = name
        self.quantum = quantum
        self.processes = PriorityQueue() # Cola con prioridad, dada por Python

    def add_process(self, process: Process):
        """
        Añade un proceso a la cola.

        El proceso se inserta en la `PriorityQueue`, ordenándose automáticamente según el valor de `last_execution_time`, que rastrea el último momento en que fue ejecutado. Esto es importante para políticas como Round Robin.

        Parámetros:
        -----------
        process : Process
            El proceso que se va a añadir a la cola.
        """
        self.processes.put((process.last_execution_time, process))

    def get_process(self):
        """
        Obtiene el siguiente proceso a ejecutar desde la cola.

        Si la cola no está vacía, extrae el proceso con menor `last_execution_time`, siguiendo la lógica de la `PriorityQueue`. 
        Si la cola está vacía, retorna None.

        Retorna:
        --------
        Process:
            El siguiente proceso a ejecutar, o None si la cola está vacía.
        """
        return self.processes.get()[1] if not self.processes.empty() else None

    def is_empty(self):
        """
        Verifica si la cola está vacía.

        Retorna:
        --------
        bool:
            True si la cola no contiene procesos, False en caso contrario.
        """
        return self.processes.empty()
