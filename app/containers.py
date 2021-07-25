from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    from producers.order_producer import OrderProducer
    from producers.email_producer import EmailProducer
    from producers.report_procuder import ReportProducer

    from services.queueServices.user_service import UserService
    from services.queueServices.logger_service import LoggerService
    from services.queueServices.report_service import ReportService
    from services.queueServices.email_service import SendEmailService
    from services.queueServices.batch_report_service import BatchReportService
    from services.queueServices.fraud_detector_service import FraudDetectorService

    
    config = providers.Configuration()

    email_producer = providers.Singleton(EmailProducer)
    order_producer = providers.Singleton(OrderProducer)
    report_producer = providers.Singleton(ReportProducer)

    user_service = providers.Singleton(UserService)
    logger_service = providers.Singleton(LoggerService)
    report_service = providers.Singleton(ReportService)
    send_email_service = providers.Singleton(SendEmailService)
    batch_report_service = providers.Singleton(BatchReportService)
    fraud_detector_service = providers.Singleton(FraudDetectorService)