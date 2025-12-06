from flask import Flask, request, jsonify, session
from database import (
    InflasiCRUD,
    NilaiTukarPetaniCRUD,
    NilaiImporCRUD,
    KedalamanKemiskinanCRUD,
    PendudukUmurSekolahCRUD,
)


def register_crud_routes(server):

    @server.route("/logout", methods=["POST"])
    def logout():
        session.clear()
        return jsonify({"status": "success"})

    @server.route("/api/inflasi", methods=["GET"])
    def get_all_inflasi():
        df = InflasiCRUD.get_all()
        return jsonify(df.to_dict(orient="records"))

    @server.route("/api/inflasi/<int:id>", methods=["GET"])
    def get_inflasi(id):
        data = InflasiCRUD.get_by_id(id)
        return jsonify(data)

    @server.route("/api/inflasi", methods=["POST"])
    def create_inflasi():
        data = request.json
        new_id = InflasiCRUD.create(data)
        return (
            jsonify({"id": new_id, "message": "Data inflasi berhasil ditambahkan"}),
            201,
        )

    @server.route("/api/inflasi/<int:id>", methods=["PUT"])
    def update_inflasi(id):
        data = request.json
        InflasiCRUD.update(id, data)
        return jsonify({"message": "Data inflasi berhasil diperbarui"})

    @server.route("/api/inflasi/<int:id>", methods=["DELETE"])
    def delete_inflasi(id):
        InflasiCRUD.delete(id)
        return jsonify({"message": "Data inflasi berhasil dihapus"})

    @server.route("/api/nilai-tukar-petani", methods=["GET"])
    def get_all_ntp():
        df = NilaiTukarPetaniCRUD.get_all()
        return jsonify(df.to_dict(orient="records"))

    @server.route("/api/nilai-tukar-petani/<int:id>", methods=["GET"])
    def get_ntp(id):
        data = NilaiTukarPetaniCRUD.get_by_id(id)
        return jsonify(data)

    @server.route("/api/nilai-tukar-petani", methods=["POST"])
    def create_ntp():
        data = request.json
        new_id = NilaiTukarPetaniCRUD.create(data)
        return jsonify({"id": new_id, "message": "Data NTP berhasil ditambahkan"}), 201

    @server.route("/api/nilai-tukar-petani/<int:id>", methods=["PUT"])
    def update_ntp(id):
        data = request.json
        NilaiTukarPetaniCRUD.update(id, data)
        return jsonify({"message": "Data NTP berhasil diperbarui"})

    @server.route("/api/nilai-tukar-petani/<int:id>", methods=["DELETE"])
    def delete_ntp(id):
        NilaiTukarPetaniCRUD.delete(id)
        return jsonify({"message": "Data NTP berhasil dihapus"})

    @server.route("/api/nilai-impor", methods=["GET"])
    def get_all_impor():
        df = NilaiImporCRUD.get_all()
        return jsonify(df.to_dict(orient="records"))

    @server.route("/api/nilai-impor/<int:id>", methods=["GET"])
    def get_impor(id):
        data = NilaiImporCRUD.get_by_id(id)
        return jsonify(data)

    @server.route("/api/nilai-impor", methods=["POST"])
    def create_impor():
        data = request.json
        new_id = NilaiImporCRUD.create(data)
        return (
            jsonify({"id": new_id, "message": "Data impor berhasil ditambahkan"}),
            201,
        )

    @server.route("/api/nilai-impor/<int:id>", methods=["PUT"])
    def update_impor(id):
        data = request.json
        NilaiImporCRUD.update(id, data)
        return jsonify({"message": "Data impor berhasil diperbarui"})

    @server.route("/api/nilai-impor/<int:id>", methods=["DELETE"])
    def delete_impor(id):
        NilaiImporCRUD.delete(id)
        return jsonify({"message": "Data impor berhasil dihapus"})

    @server.route("/api/kedalaman-kemiskinan", methods=["GET"])
    def get_all_kemiskinan():
        df = KedalamanKemiskinanCRUD.get_all()
        return jsonify(df.to_dict(orient="records"))

    @server.route("/api/kedalaman-kemiskinan/<int:id>", methods=["GET"])
    def get_kemiskinan(id):
        data = KedalamanKemiskinanCRUD.get_by_id(id)
        return jsonify(data)

    @server.route("/api/kedalaman-kemiskinan", methods=["POST"])
    def create_kemiskinan():
        data = request.json
        new_id = KedalamanKemiskinanCRUD.create(data)
        return (
            jsonify({"id": new_id, "message": "Data kemiskinan berhasil ditambahkan"}),
            201,
        )

    @server.route("/api/kedalaman-kemiskinan/<int:id>", methods=["PUT"])
    def update_kemiskinan(id):
        data = request.json
        KedalamanKemiskinanCRUD.update(id, data)
        return jsonify({"message": "Data kemiskinan berhasil diperbarui"})

    @server.route("/api/kedalaman-kemiskinan/<int:id>", methods=["DELETE"])
    def delete_kemiskinan(id):
        KedalamanKemiskinanCRUD.delete(id)
        return jsonify({"message": "Data kemiskinan berhasil dihapus"})

    @server.route("/api/penduduk-umur-sekolah", methods=["GET"])
    def get_all_penduduk():
        df = PendudukUmurSekolahCRUD.get_all()
        return jsonify(df.to_dict(orient="records"))

    @server.route("/api/penduduk-umur-sekolah/<int:id>", methods=["GET"])
    def get_penduduk(id):
        data = PendudukUmurSekolahCRUD.get_by_id(id)
        return jsonify(data)

    @server.route("/api/penduduk-umur-sekolah", methods=["POST"])
    def create_penduduk():
        data = request.json
        new_id = PendudukUmurSekolahCRUD.create(data)
        return (
            jsonify({"id": new_id, "message": "Data penduduk berhasil ditambahkan"}),
            201,
        )

    @server.route("/api/penduduk-umur-sekolah/<int:id>", methods=["PUT"])
    def update_penduduk(id):
        data = request.json
        PendudukUmurSekolahCRUD.update(id, data)
        return jsonify({"message": "Data penduduk berhasil diperbarui"})

    @server.route("/api/penduduk-umur-sekolah/<int:id>", methods=["DELETE"])
    def delete_penduduk(id):
        PendudukUmurSekolahCRUD.delete(id)
        return jsonify({"message": "Data penduduk berhasil dihapus"})
