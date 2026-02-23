from flask import jsonify
from datetime import datetime
from utils.constants import HTTP_OK,HTTP_ERROR,HTTP_NO_CONTENT, HTTP_CONFLICT

# Generador de JSON automático empleando el patron Factory Method
class ResponseFactory():
    # Exito
    @staticmethod
    def ok(data = None, message = "OK", code = HTTP_OK):
        return jsonify({
            "STATUS": "OK",
            "HTTP-CODE": code,
            "MESSAGE": message,
            "DATA": data,
            "TIMESTAMP": datetime.utcnow().isoformat()
        }), code
    
    # Error durante la carga de un archivo
    @staticmethod
    def error(message = "ERROR", code = HTTP_ERROR):
        return jsonify({
            "STATUS": "ERROR",
            "HTTP-CODE": code,
            "MESSAGE": message,
            "TIMESTAMP": datetime.utcnow().isoformat()
        }), code
    
    # No hay contenido
    @staticmethod
    def no_content(message="NO CONTENT", code = HTTP_NO_CONTENT):
        return jsonify({
            "STATUS": "NO CONTENT",
            "HTTP-CODE": code,
            "MESSAGE": message,
            "TIMESTAMP": datetime.utcnow().isoformat()
        }), code

    # Conflicto
    @staticmethod
    def conflict(message="CONFLICT", code = HTTP_CONFLICT):
        return jsonify({
            "STATUS": "CONFLICT",
            "HTTP-CODE": code,
            "MESSAGE": message,
            "TIMESTAMP": datetime.utcnow().isoformat()
        }), code
