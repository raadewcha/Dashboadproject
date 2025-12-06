import pymysql
from pymysql.cursors import DictCursor
import pandas as pd
from contextlib import contextmanager
from sqlalchemy import create_engine
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "491",
    "charset": "utf8mb4",
    "cursorclass": DictCursor,
}

DATABASE_URL = "mysql+pymysql://root:@localhost/491?charset=utf8mb4"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


@contextmanager
def get_db_connection():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        yield connection
    finally:
        connection.close()


def execute_query(query, params=None, fetch=True):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            if fetch:
                return cursor.fetchall()
            conn.commit()
            return cursor.lastrowid


def get_dataframe(query, params=None):
    from sqlalchemy import text

    with engine.connect() as conn:
        return pd.read_sql(text(query), conn, params=params)


def sanitize_numeric_value(value):
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        cleaned = value.replace(",", ".").replace("%", "").strip()
        try:
            return float(cleaned) if cleaned else None
        except ValueError:
            return value
    return value


class InflasiCRUD:
    @staticmethod
    def get_all():
        return get_dataframe("SELECT * FROM inflasi ORDER BY tahun, kota")

    @staticmethod
    def get_by_id(id):
        return execute_query("SELECT * FROM inflasi WHERE id = %s", (id,))

    @staticmethod
    def create(data):
        fields = [
            "tahun",
            "kota",
            "januari",
            "februari",
            "maret",
            "april",
            "mei",
            "juni",
            "juli",
            "agustus",
            "september",
            "oktober",
            "november",
            "desember",
            "tahunan",
        ]
        numeric_fields = [
            "januari",
            "februari",
            "maret",
            "april",
            "mei",
            "juni",
            "juli",
            "agustus",
            "september",
            "oktober",
            "november",
            "desember",
            "tahunan",
        ]
        values = tuple(
            (
                sanitize_numeric_value(data.get(field))
                if field in numeric_fields
                else data.get(field)
            )
            for field in fields
        )
        query = """INSERT INTO inflasi (tahun, kota, januari, februari, maret, april, mei, juni, 
                   juli, agustus, september, oktober, november, desember, tahunan) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        return execute_query(query, values, fetch=False)

    @staticmethod
    def update(id, data):
        fields = [
            "tahun",
            "kota",
            "januari",
            "februari",
            "maret",
            "april",
            "mei",
            "juni",
            "juli",
            "agustus",
            "september",
            "oktober",
            "november",
            "desember",
            "tahunan",
        ]
        numeric_fields = [
            "januari",
            "februari",
            "maret",
            "april",
            "mei",
            "juni",
            "juli",
            "agustus",
            "september",
            "oktober",
            "november",
            "desember",
            "tahunan",
        ]
        values = tuple(
            (
                sanitize_numeric_value(data.get(field))
                if field in numeric_fields
                else data.get(field)
            )
            for field in fields
        )
        query = """UPDATE inflasi SET tahun=%s, kota=%s, januari=%s, februari=%s, maret=%s, 
                   april=%s, mei=%s, juni=%s, juli=%s, agustus=%s, september=%s, oktober=%s, 
                   november=%s, desember=%s, tahunan=%s WHERE id=%s"""
        return execute_query(query, (*values, id), fetch=False)

    @staticmethod
    def delete(id):
        return execute_query("DELETE FROM inflasi WHERE id = %s", (id,), fetch=False)


class NilaiTukarPetaniCRUD:
    @staticmethod
    def get_all():
        return get_dataframe(
            "SELECT * FROM nilai_tukar_petani ORDER BY tahun, jenis_ntp"
        )

    @staticmethod
    def get_by_id(id):
        return execute_query("SELECT * FROM nilai_tukar_petani WHERE id = %s", (id,))

    @staticmethod
    def create(data):
        fields = [
            "tahun",
            "jenis_ntp",
            "januari",
            "februari",
            "maret",
            "april",
            "mei",
            "juni",
            "juli",
            "agustus",
            "september",
            "oktober",
            "november",
            "desember",
            "tahunan",
        ]
        numeric_fields = [
            "januari",
            "februari",
            "maret",
            "april",
            "mei",
            "juni",
            "juli",
            "agustus",
            "september",
            "oktober",
            "november",
            "desember",
            "tahunan",
        ]
        values = tuple(
            (
                sanitize_numeric_value(data.get(field))
                if field in numeric_fields
                else data.get(field)
            )
            for field in fields
        )
        query = """INSERT INTO nilai_tukar_petani (tahun, jenis_ntp, januari, februari, maret, 
                   april, mei, juni, juli, agustus, september, oktober, november, desember, tahunan) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        return execute_query(query, values, fetch=False)

    @staticmethod
    def update(id, data):
        fields = [
            "tahun",
            "jenis_ntp",
            "januari",
            "februari",
            "maret",
            "april",
            "mei",
            "juni",
            "juli",
            "agustus",
            "september",
            "oktober",
            "november",
            "desember",
            "tahunan",
        ]
        numeric_fields = [
            "januari",
            "februari",
            "maret",
            "april",
            "mei",
            "juni",
            "juli",
            "agustus",
            "september",
            "oktober",
            "november",
            "desember",
            "tahunan",
        ]
        values = tuple(
            (
                sanitize_numeric_value(data.get(field))
                if field in numeric_fields
                else data.get(field)
            )
            for field in fields
        )
        query = """UPDATE nilai_tukar_petani SET tahun=%s, jenis_ntp=%s, januari=%s, februari=%s, 
                   maret=%s, april=%s, mei=%s, juni=%s, juli=%s, agustus=%s, september=%s, oktober=%s, 
                   november=%s, desember=%s, tahunan=%s WHERE id=%s"""
        return execute_query(query, (*values, id), fetch=False)

    @staticmethod
    def delete(id):
        return execute_query(
            "DELETE FROM nilai_tukar_petani WHERE id = %s", (id,), fetch=False
        )


class NilaiImporCRUD:
    @staticmethod
    def get_all():
        return get_dataframe("SELECT * FROM nilai_impor ORDER BY tahun, bulan")

    @staticmethod
    def get_by_id(id):
        return execute_query("SELECT * FROM nilai_impor WHERE id = %s", (id,))

    @staticmethod
    def create(data):
        fields = ["tahun", "bulan", "nilai"]
        values = tuple(
            (
                sanitize_numeric_value(data.get(field))
                if field == "nilai"
                else data.get(field)
            )
            for field in fields
        )
        query = "INSERT INTO nilai_impor (tahun, bulan, nilai) VALUES (%s, %s, %s)"
        return execute_query(query, values, fetch=False)

    @staticmethod
    def update(id, data):
        fields = ["tahun", "bulan", "nilai"]
        values = tuple(
            (
                sanitize_numeric_value(data.get(field))
                if field == "nilai"
                else data.get(field)
            )
            for field in fields
        )
        query = "UPDATE nilai_impor SET tahun=%s, bulan=%s, nilai=%s WHERE id=%s"
        return execute_query(query, (*values, id), fetch=False)

    @staticmethod
    def delete(id):
        return execute_query(
            "DELETE FROM nilai_impor WHERE id = %s", (id,), fetch=False
        )


class KedalamanKemiskinanCRUD:
    @staticmethod
    def get_all():
        return get_dataframe(
            "SELECT * FROM kedalaman_kemiskinan ORDER BY tahun, kabupaten_kota"
        )

    @staticmethod
    def get_by_id(id):
        return execute_query("SELECT * FROM kedalaman_kemiskinan WHERE id = %s", (id,))

    @staticmethod
    def create(data):
        fields = ["tahun", "kabupaten_kota", "indeks"]
        values = tuple(
            (
                sanitize_numeric_value(data.get(field))
                if field == "indeks"
                else data.get(field)
            )
            for field in fields
        )
        query = "INSERT INTO kedalaman_kemiskinan (tahun, kabupaten_kota, indeks) VALUES (%s, %s, %s)"
        return execute_query(query, values, fetch=False)

    @staticmethod
    def update(id, data):
        fields = ["tahun", "kabupaten_kota", "indeks"]
        values = tuple(
            (
                sanitize_numeric_value(data.get(field))
                if field == "indeks"
                else data.get(field)
            )
            for field in fields
        )
        query = "UPDATE kedalaman_kemiskinan SET tahun=%s, kabupaten_kota=%s, indeks=%s WHERE id=%s"
        return execute_query(query, (*values, id), fetch=False)

    @staticmethod
    def delete(id):
        return execute_query(
            "DELETE FROM kedalaman_kemiskinan WHERE id = %s", (id,), fetch=False
        )


class PendudukUmurSekolahCRUD:
    @staticmethod
    def get_all():
        return get_dataframe(
            "SELECT * FROM penduduk_umur_sekolah ORDER BY tahun, kelompok_umur"
        )

    @staticmethod
    def get_by_id(id):
        return execute_query("SELECT * FROM penduduk_umur_sekolah WHERE id = %s", (id,))

    @staticmethod
    def create(data):
        fields = [
            "tahun",
            "kelompok_umur",
            "tidak_belum_sekolah",
            "masih_sekolah",
            "tidak_sekolah_lagi",
        ]
        numeric_fields = ["tidak_belum_sekolah", "masih_sekolah", "tidak_sekolah_lagi"]
        values = tuple(
            (
                sanitize_numeric_value(data.get(field))
                if field in numeric_fields
                else data.get(field)
            )
            for field in fields
        )
        query = """INSERT INTO penduduk_umur_sekolah (tahun, kelompok_umur, tidak_belum_sekolah, 
                   masih_sekolah, tidak_sekolah_lagi) VALUES (%s, %s, %s, %s, %s)"""
        return execute_query(query, values, fetch=False)

    @staticmethod
    def update(id, data):
        fields = [
            "tahun",
            "kelompok_umur",
            "tidak_belum_sekolah",
            "masih_sekolah",
            "tidak_sekolah_lagi",
        ]
        numeric_fields = ["tidak_belum_sekolah", "masih_sekolah", "tidak_sekolah_lagi"]
        values = tuple(
            (
                sanitize_numeric_value(data.get(field))
                if field in numeric_fields
                else data.get(field)
            )
            for field in fields
        )
        query = """UPDATE penduduk_umur_sekolah SET tahun=%s, kelompok_umur=%s, tidak_belum_sekolah=%s, 
                   masih_sekolah=%s, tidak_sekolah_lagi=%s WHERE id=%s"""
        return execute_query(query, (*values, id), fetch=False)

    @staticmethod
    def delete(id):
        return execute_query(
            "DELETE FROM penduduk_umur_sekolah WHERE id = %s", (id,), fetch=False
        )
