from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated  
from rest_framework_simplejwt.authentication import JWTAuthentication 
from .models import Event, EventParticipant
from django.utils.dateparse import parse_datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #i always use djangos own paginator

# Create your views here.


def check_event_owner(user, event_id):
        is_owner = EventParticipant.objects.filter(user=user, event_id=event_id, role='OWNER').exists()
        if is_owner:
            event = Event.objects.filter(id=event_id).first()
            return event, True
        return None, False
class EventView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,]

    def post(self,request):
        try:
            user = request.user 
            data = request.data
            if not user:
                return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            title = data.get('title')
            description = data.get('description')
            start_time = data.get('start_time')
            end_time = data.get('end_time')
            location = data.get('location')
            is_recurring = data.get('is_recurring', False)
            recurrence_pattern = data.get('recurrence_pattern')

            event = Event.objects.create(
                title=title,
                description=description,
                start_time=parse_datetime(start_time),
                end_time=parse_datetime(end_time),
                location=location,
                is_recurring=is_recurring,
                recurrence_pattern=recurrence_pattern
            )

            EventParticipant.objects.create(user = user, event = event, role = 'OWNER')
            return Response({
                "message": "Event created successfully",
                "event": {
                    "id": event.id,
                    "title": event.title,
                    "description": event.description,
                    "start_time": event.start_time,
                    "end_time": event.end_time,
                    "location": event.location,
                    "is_recurring": event.is_recurring,
                    "recurrence_pattern": event.recurrence_pattern,
                    "owner_id": user.id
                },
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Error in creating event"-str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request):
        try:
            user = request.user
            query = Event.objects.filter(eventparticipant__user=user) # i used through(new to me as new version of django)
                                                                    #otherwise i would query like participants__id=user

            title = request.query_params.get('title')
            if title:
                query = query.filter(title__icontains=title)

            page = request.query_params.get('page', 1)
            per_page = request.query_params.get('page_size', 10)

            paginator = Paginator(query, per_page)
            try:
                paginated_qs = paginator.page(page)
            except PageNotAnInteger:
                paginated_qs = paginator.page(1)
            except EmptyPage:
                paginated_qs = []

            data = [{
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "start_time": event.start_time,
                "end_time": event.end_time,
                "location": event.location,
                "is_recurring": event.is_recurring,
                "recurrence_pattern": event.recurrence_pattern,
            } for event in paginated_qs]

            return Response({
                "results": data,
                "count": paginator.count,
                "num_pages": paginator.num_pages,
                "current_page": int(page)
            })
        except Exception as e:
            return Response({"error in gettinggg events": str(e)}, status=status.HTTP_400_BAD_REQUEST)




class EventDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # Check if the user is the owner of the event

    def get(self, request, id):
        user = request.user
        try:
            event = Event.objects.get(id=id, eventparticipant__user=user)
            return Response({
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "start_time": event.start_time,
                "end_time": event.end_time,
                "location": event.location,
                "is_recurring": event.is_recurring,
                "recurrence_pattern": event.recurrence_pattern,
            })
        except Event.DoesNotExist:
            return Response({"error": "event not present or unau thorized"}, status=404)
    
    def put(self, request, id):
        user = request.user
        try:
            event, is_event_owner = check_event_owner(user, id)
            if not is_event_owner:
                return Response({"error": "Not authorized to edit this event"}, status=403)
        except Exception as e:
            return Response({"error": "Event not found or only owner can edit"}, status=403)

        data = request.data
        event.title = data.get("title", event.title)
        event.description = data.get("description", event.description)
        event.start_time = parse_datetime(data.get("start_time")) or event.start_time
        event.end_time = parse_datetime(data.get("end_time")) or event.end_time
        event.location = data.get("location", event.location)
        event.is_recurring = data.get("is_recurring", event.is_recurring)
        event.recurrence_pattern = data.get("recurrence_pattern", event.recurrence_pattern)
        event.save()

        return Response({"message": "Event updated successfully"})
    
    def delete(self, request, id):
        user = request.user
        try:
            event, is_event_owner = check_event_owner(user, id)
            if not is_event_owner:
                return Response({"error": "Not authorized to edit this event"}, status=403)
        except Event.DoesNotExist:
            return Response({"error": "Not authorized or event not found"}, status=403)

        event.delete()
        return Response({"message": "Event deleted successfully"})


class BulkEventView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self,request):   
        try:
            user = request.user
            event_data = request.data
            if not isinstance(event_data,list):
                return Response({"error": "Invalid data format. Expect a list format"}, status=status.HTTP_400_BAD_REQUEST)
            
            events_to_create = []
            participants_to_create = []
            created_events_response = []
            errors = [] 

            for idx,data in enumerate(event_data):
                try:
                    title = data.get('title')
                    description = data.get('description')
                    start_time = data.get('start_time')
                    end_time = data.get('end_time')
                    location = data.get('location')
                    is_recurring = data.get('is_recurring', False)
                    recurrence_pattern = data.get('recurrence_pattern')
                    if not title or not start_time or not end_time:
                        raise ValueError("Missing required fields: title, start_time, end_time")

                    event = Event(
                        title=title,
                        description=description,
                        start_time=parse_datetime(start_time),
                        end_time=parse_datetime(end_time),
                        location=location,
                        is_recurring=is_recurring,
                        recurrence_pattern=recurrence_pattern
                    )
                    events_to_create.append(event)
                except Exception as e:
                    errors.append({"error": f"Error in creating event {idx+1}: {str(e)}"})

            created_events = Event.objects.bulk_create(events_to_create)

    # Create eventparticipant owner entries
            for event in created_events:
                participants_to_create.append(EventParticipant(user=user, event=event, role='OWNER'))
                created_events_response.append({
                    "id": event.id,
                    "title": event.title,
                    "start_time": event.start_time,
                    "end_time": event.end_time,
                })

            EventParticipant.objects.bulk_create(participants_to_create)

            return Response({
                "created_events": created_events_response,
                "errors": errors
            }, status=201 if created_events else 400)
        except Exception as e:  
            return Response({"erroe in bulk event creation ": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class EventViewShare(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, id):
        from django.contrib.auth import get_user_model
        user = request.user
        data = request.data.get("users", [])

        if not isinstance(data,list):
            return Response({"error": "Invalid data format. Expect a list format"}, status=status.HTTP_400_BAD_REQUEST)

        try:

            event, is_event_owner = check_event_owner(user, id)
            if not is_event_owner:
                return Response({"error": "Not authorized to share this event"}, status=403)
            
            valid_roles = ['OWNER', 'EDITOR', 'VIEWER']
            User = get_user_model()


            for entry in data:
                user_id = entry.get("user_id")
                role = entry.get("role")

                if not user_id or role not in valid_roles:
                    return Response({"error": f"Invalid entry: {entry}"}, status=400)

                requested_user = User.objects.get(id=user_id)
        
                if not requested_user:
                    return Response({"error": f"User with id {user_id} does not exist"}, status=400)
                
                if requested_user.id == user.id:
                    continue   #ignoring current suer as already granted permission
                EventParticipant.objects.update_or_create(
                    event_id=id,
                    user=requested_user,
                    defaults={"role": role}
                )

            # Return updated permission list
            participants = EventParticipant.objects.filter(event_id=id).select_related("user")
            permissions = [{
                "user_id": p.user.id,
                "username": p.user.username,
                "role": p.role
            } for p in participants]

            return Response({"message": "Event shared successfully", "permissions": permissions}, status=200)

        except Exception as e:
            return Response({"error in sharing event permission": str(e)}, status=400)

    def get(self, request, id):
        # any user can view the permissions 
        participants = EventParticipant.objects.filter(event_id=id).select_related("user")
        data = [
            {"user_id": p.user.id, "username": p.user.username, "role": p.role}
            for p in participants
        ]
        return Response({"participants": data}, status=200)
    
    def put(self, request, id, user_id):
        user = request.user
        try:
            # Only owners can update permissions
            EventParticipant.objects.get(event_id=id, user=user, role='OWNER')
        except EventParticipant.DoesNotExist:
            return Response({"error": "Only event owners can update permissions."}, status=403)

        try:
            participant = EventParticipant.objects.get(event_id=id, user_id=user_id)
        except EventParticipant.DoesNotExist:
            return Response({"error": "Participant not found for this event."}, status=404)

        role = request.data.get("role")
        if role not in ['OWNER','EDITOR', 'VIEWER']:
            return Response({"error": "Invalid role. Use 'EDITOR' or 'VIEWER'."}, status=400)

        participant.role = role
        participant.save()

        return Response({"message": "User permission updated", "user_id": user_id, "role": role}, status=200)
    
    def delete(self, request, id, user_id):
        user = request.user

        # Check if request.user is the owner
        is_owner = EventParticipant.objects.filter(event_id=id, user=user, role='O').exists()
        if not is_owner:
            return Response({"error": "Only the event owner can remove participants."}, status=status.HTTP_403_FORBIDDEN)

        # Cannot remove self
        if user.id == user_id:
            return Response({"error": "Owner cannot remove themselves from the event."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            participant = EventParticipant.objects.get(event_id=id, user_id=user_id)
            participant.delete()
            return Response({"message": "User removed from the event."}, status=status.HTTP_200_OK)
        except EventParticipant.DoesNotExist:
            return Response({"error": "User not found in the event."}, status=status.HTTP_404_NOT_FOUND)