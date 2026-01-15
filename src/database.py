"""
Database integration layer (PostgreSQL/MongoDB)
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///guardrail.db')  # Fallback to SQLite

# Create engine
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Models
class RegulatoryUpdate(Base):
    """Regulatory update model"""
    __tablename__ = 'regulatory_updates'
    
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(100), index=True, nullable=False)
    source = Column(String(200), nullable=False)
    title = Column(String(500), nullable=False)
    summary = Column(Text)
    url = Column(String(1000))
    confidence = Column(String(20))  # high, medium, low
    status = Column(String(50))  # pending_review, approved, implemented
    detected_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ComplianceScan(Base):
    """Compliance scan result model"""
    __tablename__ = 'compliance_scans'
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(String(100), index=True)
    country = Column(String(100), index=True)
    compliant = Column(Boolean, nullable=False)
    violations = Column(JSON)  # Store as JSON
    warnings = Column(JSON)
    scan_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class PolicyRule(Base):
    """Policy rule model"""
    __tablename__ = 'policy_rules'
    
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(100), index=True, nullable=False)
    category = Column(String(100))  # forbidden_keywords, time_restrictions, etc.
    rule_data = Column(JSON, nullable=False)
    active = Column(Boolean, default=True)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AuditLog(Base):
    """Audit log model"""
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(100), nullable=False)
    component = Column(String(100))
    details = Column(JSON)
    user = Column(String(100))
    ip_address = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)


# Database operations
class DatabaseManager:
    """Database manager with common operations"""
    
    def __init__(self):
        self.session = SessionLocal()
    
    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(bind=engine)
    
    def add_regulatory_update(self, country, source, title, **kwargs):
        """Add new regulatory update"""
        update = RegulatoryUpdate(
            country=country,
            source=source,
            title=title,
            **kwargs
        )
        self.session.add(update)
        self.session.commit()
        return update
    
    def get_recent_updates(self, days=30, country=None):
        """Get recent regulatory updates"""
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        query = self.session.query(RegulatoryUpdate).filter(
            RegulatoryUpdate.detected_at >= cutoff
        )
        
        if country:
            query = query.filter(RegulatoryUpdate.country == country)
        
        return query.order_by(RegulatoryUpdate.detected_at.desc()).all()
    
    def add_compliance_scan(self, content_id, country, compliant, violations=None, warnings=None):
        """Add compliance scan result"""
        scan = ComplianceScan(
            content_id=content_id,
            country=country,
            compliant=compliant,
            violations=violations or [],
            warnings=warnings or []
        )
        self.session.add(scan)
        self.session.commit()
        return scan
    
    def log_action(self, action, component=None, details=None, user=None, ip=None):
        """Log an action to audit log"""
        log = AuditLog(
            action=action,
            component=component,
            details=details or {},
            user=user,
            ip_address=ip
        )
        self.session.add(log)
        self.session.commit()
        return log
    
    def close(self):
        """Close database session"""
        self.session.close()


# Migration helper
def run_migrations():
    """Run database migrations"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == '__main__':
    # Initialize database
    run_migrations()
    print(f"Database initialized at: {DATABASE_URL}")
