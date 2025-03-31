from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity,get_jwt
from datetime import datetime, timedelta
from .models import *
from .custom import custom_email
import random
from sqlalchemy.orm import joinedload
from flask_caching import Cache
cache=Cache()
class ServiceListAPI(Resource):
    @cache.cached(timeout=10)
    def get(self):
        search_query = request.args.get('search')
        services = Service.query
        if search_query:
            services = services.filter(Service.name.ilike(f'%{search_query}%'))
        return {
            'services': [{
                'id': s.id,
                'name': s.name,
                'description': s.description,
                'base_price': s.base_price,
                'time_required': s.time_required
            } for s in services.all()]
        }, 200

class ServiceRequestAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=10)
    def get(self):
        current_user = User.query.get(get_jwt_identity())
        if current_user.role == 'customer':
            requests = ServiceRequest.query.filter_by(customer_id=current_user.customer_profile.id)
        elif current_user.role == 'professional':
            requests = ServiceRequest.query.filter_by(professional_id=current_user.professional_profile.id)
        else:
            return {"message": "Unauthorized"}, 403
        today = datetime.utcnow().date()
        scheduled_today = []
        ongoing_services = []
        completed_services = []
        requested_services = []
        accepted_services = []
        rejected_services = []
        for req in requests.all():
            date_of_completion = req.date_of_completion.strftime('%Y-%m-%d %H:%M:%S') if req.date_of_completion else None
            customer_address = req.customer.address
            service_amount = req.service.base_price
            request_data = {
                "id": req.id,
                "service_name": req.service.name,
                "city": req.city.name,
                "address": customer_address, 
                "status": req.service_status,
                "requested_date": req.date_of_request.strftime('%Y-%m-%d'),
                "date_of_completion": date_of_completion,
                "amount": service_amount 
            }
            if current_user.role == 'customer' and req.customer_id == current_user.customer_profile.id:
                request_data["pin"] = req.pin
            if req.service_status == 'scheduled' and req.date_of_completion and req.date_of_completion.date() == today:
                scheduled_today.append(request_data)
            elif req.service_status in ['in_progress', 'started']:
                ongoing_services.append(request_data)
            elif req.service_status in ['completed', 'closed']:
                completed_services.append(request_data)
            elif req.service_status == 'requested':
                requested_services.append(request_data)
            elif req.service_status == 'scheduled':
                accepted_services.append(request_data)
            elif req.service_status == 'rejected':
                rejected_services.append(request_data)
        return {
            "requested_services": requested_services,
            "accepted_services": accepted_services,
            "rejected_services": rejected_services,
            "scheduled_today": scheduled_today,
            "ongoing_services": ongoing_services,
            "completed_services": completed_services
        }, 200
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user.role != 'customer':
            return {"message": "Unauthorized"}, 403
        customer = Customer.query.filter_by(user_id=user.id).first()
        if not customer:
            return {"message": "Customer not found"}, 400
        city_id = customer.city_id 
        data = request.get_json()
        service = Service.query.get(data.get('service_id'))
        if not service:
            return {"message": "Service not found"}, 404
        professional = ServiceProfessional.query.filter_by(id=data.get('professional_id')).first()
        if not professional:
            return {"message": "Professional not found"}, 404
        date_of_completion = data.get("date_of_completion")
        if date_of_completion:
            try:
                date_of_completion = datetime.strptime(date_of_completion, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return {"message": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'"}, 400
        else:
            date_of_completion = None
        new_request = ServiceRequest(
            service_id=service.id,
            customer_id=customer.id,
            professional_id=professional.id,
            date_of_request=datetime.utcnow(),  
            date_of_completion=date_of_completion,
            service_status='requested',
            pin=random.randint(1000, 9999),  
            city_id=city_id  
        )

        db.session.add(new_request)
        db.session.commit()

        return {
            "message": "Service request created successfully",
            "request_id": new_request.id
        }, 201

    @jwt_required()
    def put(self, request_id):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if user.role != 'customer':
            return {"message": "Unauthorized"}, 403

        service_request = ServiceRequest.query.get(request_id)
        if not service_request:
            return {"message": "Service request not found"}, 404

        if service_request.customer_id != user.customer_profile.id:
            return {"message": "Unauthorized"}, 403

        if service_request.service_status == 'mark_reached':
            return {"message": "Cannot update after professional has marked as reached"}, 400

        data = request.get_json()
        service_request.date_of_completion = datetime.strptime(
            data.get("date_of_completion"), "%Y-%m-%d %H:%M:%S"
        ) if data.get("date_of_completion") else service_request.date_of_completion

        service_request.professional_id = data.get("professional_id", service_request.professional_id)

        db.session.commit()
        return {"message": "Service request updated"}, 200

    @jwt_required()
    def delete(self, request_id):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        service_request = ServiceRequest.query.get(request_id)
        if not service_request:
            return {"message": "Service request not found"}, 404

        
        if user.role == 'customer' :
            if service_request.service_status == 'mark_reached':
                return {"message": "Cannot cancel after professional has marked as reached"}, 400
            db.session.delete(service_request)
            db.session.commit()
            return {"message": "Service request canceled"}, 200

        
        elif user.role == 'professional' and service_request.professional_id == user.id:
            if service_request.date_of_completion and service_request.date_of_completion <= datetime.utcnow():
                return {"message": "Cannot delete request after completion date"}, 400
            db.session.delete(service_request)
            db.session.commit()
            return {"message": "Service request deleted"}, 200

        return {"message": "Unauthorized"}, 403

    @jwt_required()
    def patch(self, request_id):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        service_request = ServiceRequest.query.get(request_id)

        if not service_request:
            return {'message': 'Service request not found'}, 404

        data = request.get_json()
        action = data.get('action')

        if not action:
            return {'message': 'Action is required'}, 400

        
        if user.role == 'professional':
            
            if not user.professional_profile or service_request.professional_id != user.professional_profile.id:
                return {"message": "Unauthorized"}, 403

            if action == 'accept':
                service_request.service_status = 'scheduled'

            elif action == 'reject':
                service_request.service_status = 'rejected'

            elif action == 'mark_reached':
                service_request.service_status = 'in_progress'

            elif action == 'start':
                pin = data.get('pin')
                if pin is None or not str(pin).isdigit():
                    return {'message': 'PIN is required and must be numeric'}, 400
                if int(pin) != service_request.pin:
                    return {'message': 'Invalid PIN'}, 400
                service_request.service_status = 'started'
                db.session.commit()
                return {'message': 'Service Started'}, 200

            elif action == 'complete':
                service_request.service_status = 'completed'
                service_request.date_of_completion = datetime.utcnow()
                transaction = Transaction(
                    customer_id=service_request.customer_id,
                    service_request_id=service_request.id,
                    amount=service_request.service.base_price,
                    payment_status='pending'
                )
                db.session.add(transaction)

            elif action == 'transaction_complete':
                transaction = Transaction.query.filter_by(service_request_id=service_request.id).first()
                if not transaction:
                    return {"message": "Transaction not found"}, 404
                transaction.payment_status = 'completed'
                transaction.date_of_transaction = datetime.utcnow()
                transaction.method = data.get("method", "Unknown")
                service_request.service_status = 'closed'
                db.session.commit()
                return {"message": "Transaction done, service completed"}, 200

            db.session.commit()
            return {'message': 'Service request updated'}, 200

        return {'message': 'Unauthorized'}, 403

class ProfessionalDashboardAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=10)
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role != "professional":
            return {"message": "User is not a professional"}, 403

        
        professional = user.professional_profile
        if not professional:
            return {"message": "Professional profile not found"}, 404

        
        requests = ServiceRequest.query.filter_by(professional_id=professional.id).all()

        
        transactions = Transaction.query.join(ServiceRequest).filter(ServiceRequest.professional_id == professional.id).all()

        return {
            'requests': [{
                'id': r.id,
                'service_name': r.service.name,
                'customer_name': r.customer.name,
                'status': r.service_status,
                'date': r.date_of_request.strftime('%Y-%m-%d')
            } for r in requests],

            'transactions': [{
                'id': t.id,
                'amount': t.amount,
                'status': t.payment_status,
                'date': t.transaction_date.strftime('%Y-%m-%d') if t.transaction_date else None
            } for t in transactions]
        }, 200

class GetProfessionalsAPI(Resource):
    @jwt_required()
    def post(self):
        user = User.query.get(get_jwt_identity())
        if user.role != "customer":
            return {"message": "Unauthorized"}, 403

        
        customer = Customer.query.filter_by(user_id=user.id).first()
        if not customer:
            return {"message": "Customer profile not found"}, 404

        city_id = customer.city_id  
        data = request.get_json()
        service_type = data.get("service_type")

        if not service_type:
            return {"message": "service_type is required"}, 400

        professionals = (
            ServiceProfessional.query
            .filter_by(city_id=city_id, service_type=service_type)
            .join(User)
            .filter(User.is_verified == True, User.is_blocked == False)
            .all()
        )

        if not professionals:
            return {"message": "No professionals found for this city and service type"}, 404

        return {
            "professionals": [{
                "id": p.id,
                "user_id": p.user_id,
                "name": p.name,
                "email": p.email,
                "phone": p.phone,
                "service_type": p.service_type,
                "experience": p.experience,
                "rating": p.rating,
                "registered_on": p.registered_on.strftime('%Y-%m-%d'),
                "city": p.city.name
            } for p in professionals]
        }, 200

class AdminUserManagementAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=10)
    def get(self):
        user = User.query.get(get_jwt_identity())
        if user.role != 'admin':
            return {"message": "Unauthorized"}, 403

        
        customers = Customer.query.join(User).filter(User.role == "customer").all()
        customers_data = [{
            "id": c.id,  
            "user_id": c.user_id,  
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "address": c.address,
            "registered_on": c.registered_on.strftime('%Y-%m-%d %H:%M:%S'),
            "city": c.city.name,
            "is_blocked": c.user.is_blocked
        } for c in customers]

        
        professionals = ServiceProfessional.query.join(User).filter(User.role == "professional").all()
        professionals_data = [{
            "id": p.id,  
            "user_id": p.user_id,  
            "name": p.name,
            "email": p.email,
            "phone": p.phone,
            "service_type": p.service_type,
            "experience": p.experience,
            "rating": p.rating,
            "registered_on": p.registered_on.strftime('%Y-%m-%d %H:%M:%S'),
            "city": p.city.name,
            "is_blocked": p.user.is_blocked,
            "is_verified": p.user.is_verified
        } for p in professionals]

        
        unverified_professionals = [p for p in professionals_data if not p["is_verified"]]

        return {
            "customers": customers_data,
            "professionals": professionals_data,
            "unverified_professionals": unverified_professionals
        }, 200

    @jwt_required()
    def patch(self, user_id):
        admin_user = User.query.get(get_jwt_identity())
        if admin_user.role != 'admin':
            return {"message": "Unauthorized"}, 403

        user = User.query.get(user_id)  
        if not user:
            return {"message": "User not found"}, 404

        data = request.get_json()
        status = data.get('status')

        if status == "verified":
            user.is_verified = True
        elif status == "blocked":
            user.is_blocked = True
        elif status == "unblocked":
            user.is_blocked = False
        else:
            return {"message": "Invalid status"}, 400

        db.session.commit()
        
        print(f"Updated User {user.id}: is_verified = {user.is_verified}, is_blocked = {user.is_blocked}")

        return {"message": f"User {user_id} status updated to {status}"}, 200

class ServiceManagementAPI(Resource):

    @jwt_required()
    @cache.cached(timeout=10)
    def get(self):
        user = User.query.get(get_jwt_identity())
        
        if user.role == 'admin':
            requests = ServiceAdditionRequest.query.filter_by(status="pending").all()
        elif user.role == 'professional':
            requests = ServiceAdditionRequest.query.filter_by(professional_id=user.professional_profile.id).all()
        else:
            return {"message": "Unauthorized"}, 403
        
        return {"requests": [{
            "id": req.id,
            "name": req.name,
            "description": req.description,
            "base_price": req.base_price,
            "time_required": req.time_required,
            "status": req.status
        } for req in requests]}, 200

    @jwt_required()
    def post(self):
        user = User.query.get(get_jwt_identity())
        data = request.get_json()
        
        if user.role == "admin":
            new_service = Service(
                name=data.get("name"),
                description=data.get("description"),
                base_price=data.get("base_price"),
                time_required=data.get("time_required")
            )
            db.session.add(new_service)
            db.session.commit()
            return {"message": "Service created"}, 201
        
        elif user.role == "professional":
            new_request = ServiceAdditionRequest(
                professional_id=user.professional_profile.id,
                name=data.get("name"),
                description=data.get("description"),
                base_price=data.get("base_price"),
                time_required=data.get("time_required"),
                status="pending"
            )
            db.session.add(new_request)
            db.session.commit()
            return {"message": "Service addition request submitted", "request_id": new_request.id}, 201
        
        return {"message": "Unauthorized"}, 403

    @jwt_required()
    def put(self, request_id):
        user = User.query.get(get_jwt_identity())
        data = request.get_json()

        if user.role == 'admin':
            service = Service.query.get(request_id)
            if not service:
                return {"message": "Service not found"}, 404
            
            service.name = data.get("name", service.name)
            service.description = data.get("description", service.description)
            service.base_price = data.get("base_price", service.base_price)
            service.time_required = data.get("time_required", service.time_required)
            
            db.session.commit()
            return {"message": "Service updated"}, 200
        
        elif user.role == 'professional':
            service_request = ServiceAdditionRequest.query.get(request_id)
            if not service_request or service_request.status != "pending":
                return {"message": "Cannot update this request"}, 400
            
            service_request.name = data.get("name", service_request.name)
            service_request.description = data.get("description", service_request.description)
            service_request.base_price = data.get("base_price", service_request.base_price)
            service_request.time_required = data.get("time_required", service_request.time_required)
            
            db.session.commit()
            return {"message": "Service addition request updated"}, 200
        
        return {"message": "Unauthorized"}, 403

    @jwt_required()
    def patch(self, request_id):
        user = User.query.get(get_jwt_identity())
        if user.role != 'admin':
            return {"message": "Unauthorized"}, 403

        service_request = ServiceAdditionRequest.query.get(request_id)
        if not service_request:
            return {"message": "Request not found"}, 404

        data = request.get_json()
        status = data.get("status")

        if status not in ["approved", "rejected"]:
            return {"message": "Invalid status"}, 400

        service_request.status = status

        if status == "approved":
            
            new_service = Service(
                name=service_request.name,
                description=service_request.description,
                base_price=service_request.base_price,
                time_required=service_request.time_required
            )
            db.session.add(new_service)

        db.session.commit()
        return {"message": f"Service request {status} and added to services" if status == "approved" else f"Service request {status}"}, 200
    @jwt_required()
    def delete(self, request_id):
        user = User.query.get(get_jwt_identity())
        
        if user.role == 'admin':
            service = Service.query.get(request_id)
            if not service:
                return {"message": "Service not found"}, 404
            
            db.session.delete(service)
            db.session.commit()
            return {"message": "Service deleted"}, 200
        
        elif user.role == 'professional':
            service_request = ServiceAdditionRequest.query.get(request_id)
            if not service_request or service_request.status != "pending":
                return {"message": "Cannot delete this request"}, 400
            
            db.session.delete(service_request)
            db.session.commit()
            return {"message": "Service request deleted"}, 200
        
        return {"message": "Unauthorized"}, 403

class ProfessionalProfileAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=10)
    def get(self):
        user = User.query.get(get_jwt_identity())
        if user.role != 'professional':
            return {"message": "Unauthorized"}, 403

        professional = ServiceProfessional.query.filter_by(user_id=user.id).first()
        if not professional:
            return {"message": "Profile not found"}, 404

        return {
            "id": professional.id,
            "name": professional.name,
            "email": professional.email,
            "phone": professional.phone,
            "service_type": professional.service_type,
            "experience": professional.experience,
            "city_id": professional.city_id,
            "city": professional.city.name  
        }, 200

    @jwt_required()
    def put(self):
        user = User.query.get(get_jwt_identity())
        if user.role != 'professional':
            return {"message": "Unauthorized"}, 403

        professional = ServiceProfessional.query.filter_by(user_id=user.id).first()
        if not professional:
            return {"message": "Profile not found"}, 404

        data = request.get_json()
        professional.name = data.get("name", professional.name)
        professional.phone = data.get("phone", professional.phone)
        professional.service_type = data.get("service_type", professional.service_type)
        professional.experience = data.get("experience", professional.experience)

        
        if "city_id" in data:
            city = City.query.get(data["city_id"])
            if not city:
                return {"message": "Invalid city ID"}, 400
            professional.city_id = city.id

        db.session.commit()
        return {"message": "Profile updated"}, 200

    @jwt_required()
    def delete(self):
        user = User.query.get(get_jwt_identity())
        if user.role != 'professional':
            return {"message": "Unauthorized"}, 403

        professional = ServiceProfessional.query.filter_by(user_id=user.id).first()
        if not professional:
            return {"message": "Profile not found"}, 404

        
        ServiceRequest.query.filter_by(professional_id=professional.id).update({"service_status": "canceled"})

        
        Review.query.filter_by(professional_id=professional.id).update({"professional_id": None})

        
        db.session.delete(professional)
        db.session.commit()

        return {"message": "Profile deleted, but service requests and reviews are retained"}, 200

class CustomerProfileAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=10)
    def get(self):
        user = User.query.get(get_jwt_identity())
        if user.role != 'customer':
            return {"message": "Unauthorized"}, 403

        customer = Customer.query.filter_by(user_id=user.id).first()
        if not customer:
            return {"message": "Profile not found"}, 404

        return {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
            "address": customer.address
        }, 200

    @jwt_required()
    def put(self):
        user = User.query.get(get_jwt_identity())
        if user.role != 'customer':
            return {"message": "Unauthorized"}, 403

        customer = Customer.query.filter_by(user_id=user.id).first()
        if not customer:
            return {"message": "Profile not found"}, 404

        data = request.get_json()
        customer.name = data.get("name", customer.name)
        customer.phone = data.get("phone", customer.phone)
        customer.address = data.get("address", customer.address)
        customer.city_id=data.get("city_id",customer.city_id)
        db.session.commit()
        return {"message": "Profile updated"}, 200

    @jwt_required()
    def delete(self):
        user = User.query.get(get_jwt_identity())
        if user.role != 'customer':
            return {"message": "Unauthorized"}, 403

        customer = Customer.query.filter_by(user_id=user.id).first()
        if not customer:
            return {"message": "Profile not found"}, 404

        db.session.delete(customer)
        db.session.commit()
        return {"message": "Profile deleted"}, 200

class AdminServiceRequestsAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=10)
    def get(self):
        admin_user = User.query.get(get_jwt_identity())
        if admin_user.role != 'admin':
            return {"message": "Unauthorized"}, 403
        
        today = datetime.utcnow().date()
        scheduled_today = []
        ongoing_services = []
        completed_services = []
        requested_services = []
        accepted_services = []
        rejected_services = []

        all_requests = ServiceRequest.query.all()
        
        for req in all_requests:
            service_data = {
                "id": req.id,
                "service_name": req.service.name,
                "customer_name": req.customer.name,
                "professional_name": req.professional.name if req.professional else None,
                "status": req.service_status,
                "requested_date": req.date_of_request.strftime('%Y-%m-%d'),
                "date_of_completion": req.date_of_completion.strftime('%Y-%m-%d %H:%M:%S') if req.date_of_completion else None,
                "amount": req.service.base_price  
            }
            
            if req.service_status == 'scheduled' and req.date_of_completion and req.date_of_completion.date() == today:
                scheduled_today.append(service_data)
            elif req.service_status in ['in_progress', 'started']:
                transaction = Transaction.query.filter_by(service_request_id=req.id).first()
                service_data["payment_status"] = transaction.payment_status if transaction else "pending"
                service_data["payment_method"] = transaction.method if transaction else "Unknown"
                ongoing_services.append(service_data)
            elif req.service_status in ['completed', 'closed']:
                transaction = Transaction.query.filter_by(service_request_id=req.id).first()
                # Get the review specifically for this service request
                review = Review.query.filter_by(service_request_id=req.id).first()
                service_data["payment_status"] = transaction.payment_status if transaction else "pending"
                service_data["payment_method"] = transaction.method if transaction else "Unknown"
                service_data["review"] = {
                    "rating": review.rating if review else None,
                    "comment": review.comment if review else None
                }
                completed_services.append(service_data)
            elif req.service_status == 'requested':
                requested_services.append(service_data)
            elif req.service_status == 'scheduled':  
                accepted_services.append(service_data)
            elif req.service_status == 'rejected':
                rejected_services.append(service_data)

        # Remove duplicates from completed services based on service_request_id
        seen_ids = set()
        unique_completed_services = []
        for service in completed_services:
            if service["id"] not in seen_ids:
                seen_ids.add(service["id"])
                unique_completed_services.append(service)

        return {
            "requested_services": requested_services,
            "accepted_services": accepted_services,
            "rejected_services": rejected_services,
            "scheduled_today": scheduled_today,
            "ongoing_services": ongoing_services,
            "completed_services": unique_completed_services
        }, 200

class ReviewAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=10)
    def get(self):
        current_user = User.query.get(get_jwt_identity())
        if current_user.role != "customer":
            return {"message": "Unauthorized"}, 403

        
        service_requests = (
            ServiceRequest.query
            .filter(ServiceRequest.customer_id == current_user.customer_profile.id)
            .filter(ServiceRequest.service_status.in_(["completed", "closed"]))
            .filter(~ServiceRequest.id.in_(db.session.query(Review.service_request_id)))
            .all()
        )

        return {
            "pending_reviews": [{
                "service_request_id": req.id,
                "service_name": req.service.name,
                "requested_date": req.date_of_request.strftime('%Y-%m-%d'),
                "professional_name": req.professional.name,
                "status": req.service_status
            } for req in service_requests]
        }, 200

    @jwt_required()
    def post(self, service_request_id):
        current_user = User.query.get(get_jwt_identity())
        if current_user.role != "customer":
            return {"message": "Unauthorized"}, 403

        service_request = ServiceRequest.query.get(service_request_id)
        if not service_request or service_request.customer_id != current_user.customer_profile.id:
            return {"message": "Invalid service request"}, 400
        if service_request.service_status not in ["completed", "closed"]:
            return {"message": "Review allowed only after service completion"}, 400

        data = request.get_json()
        rating = int(data.get("rating"))
        comment = data.get("comment", "")

        if not (1 <= rating <= 5):
            return {"message": "Rating must be between 1 and 5"}, 400

        
        review = Review(
            service_request_id=service_request.id,
            customer_id=service_request.customer_id,
            professional_id=service_request.professional_id,
            rating=rating,
            comment=comment
        )
        db.session.add(review)

        
        professional = ServiceProfessional.query.get(service_request.professional_id)
        if professional:
            total_reviews = Review.query.filter_by(professional_id=professional.id).count()
            total_rating = db.session.query(db.func.sum(Review.rating)).filter_by(professional_id=professional.id).scalar()
            
            if total_reviews > 0 and total_rating is not None:
                professional.rating = total_rating / total_reviews  
            
        db.session.commit()
        return {"message": "Review submitted successfully, Professional rating updated"}, 201

import csv
from flask import Response
from application.models import db, ServiceRequest, Transaction, Review, User
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from io import StringIO

class ExportServiceRequestsAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=10)
    def get(self):
        admin_user = User.query.get(get_jwt_identity())
        if admin_user.role != 'admin':
            return {"message": "Unauthorized"}, 403

        service_requests = ServiceRequest.query.filter(ServiceRequest.service_status == "closed").all()
        
        # Create CSV data
        data = [["Service ID", "Customer Name", "Professional Name", "Service Name", "Requested Date", "Completion Date", "Amount", "Payment Status", "Review"]]
        for req in service_requests:
            transaction = Transaction.query.filter_by(service_request_id=req.id).first()
            review = Review.query.filter_by(professional_id=req.professional_id, customer_id=req.customer_id).first()
            data.append([
                req.id, 
                req.customer.name, 
                req.professional.name if req.professional else "N/A",
                req.service.name, 
                req.date_of_request.strftime('%Y-%m-%d'),
                req.date_of_completion.strftime('%Y-%m-%d %H:%M:%S') if req.date_of_completion else "N/A",
                req.service.base_price,  
                transaction.payment_status if transaction else "Pending",
                f"{review.rating}/5 - {review.comment}" if review else "No review"
            ])
        
        # Create CSV string
        si = StringIO()
        writer = csv.writer(si)
        writer.writerows(data)
        output = si.getvalue()
        
        return Response(
            output,
            mimetype='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename=completed_services.csv'
            }
        )
