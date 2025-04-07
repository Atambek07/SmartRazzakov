from django.db import connection
from datetime import datetime, timedelta
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class TaleAnalytics:
    """Сбор и анализ данных об использовании историй"""
    
    def get_usage_stats(self, period_days: int = 30) -> dict:
        """Основная статистика за период"""
        stats = {
            'total_scans': 0,
            'popular_tales': [],
            'time_stats': defaultdict(int),
            'formats': defaultdict(int)
        }
        
        try:
            with connection.cursor() as cursor:
                # Общее количество сканирований
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM tale_scans 
                    WHERE scan_time >= %s
                """, [datetime.now() - timedelta(days=period_days)])
                stats['total_scans'] = cursor.fetchone()[0]
                
                # Популярные истории
                cursor.execute("""
                    SELECT tale_id, COUNT(*) as scan_count
                    FROM tale_scans
                    WHERE scan_time >= %s
                    GROUP BY tale_id
                    ORDER BY scan_count DESC
                    LIMIT 5
                """, [datetime.now() - timedelta(days=period_days)])
                stats['popular_tales'] = [
                    {'tale_id': row[0], 'scans': row[1]} 
                    for row in cursor.fetchall()
                ]
                
            return stats
            
        except Exception as e:
            logger.error(f"Analytics query failed: {str(e)}")
            return stats

    def log_scan(self, tale_id: str, user_id: str = None, format_used: str = None):
        """Логирование факта сканирования"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO tale_scans 
                    (tale_id, user_id, format_used, scan_time)
                    VALUES (%s, %s, %s, %s)
                """, [tale_id, user_id, format_used, datetime.now()])
        except Exception as e:
            logger.error(f"Failed to log scan: {str(e)}")

    def get_user_engagement(self, user_id: str) -> dict:
        """Статистика вовлеченности конкретного пользователя"""
        # Реализация аналитики по пользователю
        pass