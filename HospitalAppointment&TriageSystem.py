import heapq
import itertools
import sys

def make_queue(max_size):
    return {"data": [None] * max_size, "front": 0, "rear": -1, "count": 0, "max": max_size}

def queue_is_full(q):
    return q["count"] == q["max"]

def queue_is_empty(q):
    return q["count"] == 0

def enqueue_routine(q, token):
    if queue_is_full(q):
        return False
    q["rear"] = (q["rear"] + 1) % q["max"]
    q["data"][q["rear"]] = token
    q["count"] += 1
    return True

def dequeue_routine(q):
    if queue_is_empty(q):
        return None
    token = q["data"][q["front"]]
    q["data"][q["front"]] = None
    q["front"] = (q["front"] + 1) % q["max"]
    q["count"] -= 1
    return token

def peek_routine(q):
    if queue_is_empty(q):
        return None
    return q["data"][q["front"]]

def remove_last_from_queue(q):
    if queue_is_empty(q):
        return None
    token = q["data"][q["rear"]]
    q["data"][q["rear"]] = None
    q["rear"] = (q["rear"] - 1 + q["max"]) % q["max"]
    q["count"] -= 1
    return token

def queue_push_front(q, token):
    if queue_is_full(q):
        return False
    q["front"] = (q["front"] - 1 + q["max"]) % q["max"]
    q["data"][q["front"]] = token
    q["count"] += 1
    return True

def rebuild_queue_excluding(q, exclude_token_id):
    temp = []
    while not queue_is_empty(q):
        t = dequeue_routine(q)
        if t and t.get("token_id") != exclude_token_id:
            temp.append(t)
    for t in temp:
        enqueue_routine(q, t)
    return

def rebuild_queue_with_front(q, token):
    # Attempt to reconstruct queue with token at front. If queue full, return False.
    if queue_is_full(q):
        return False
    temp = []
    while not queue_is_empty(q):
        temp.append(dequeue_routine(q))
    enqueue_routine(q, token)
    for t in temp:
        enqueue_routine(q, t)
    return True

def make_slot(slot_id, start_time, end_time, doctor_id):
    return {"slot_id": slot_id, "start": start_time, "end": end_time, "status": "FREE", "doctor_id": doctor_id}

def make_node(slot):
    return {"slot": slot, "next": None}

def schedule_add_slot(doctor_schedules, doctor_id, slot):
    head = doctor_schedules.get(doctor_id)
    node = make_node(slot)
    if head is None:
        doctor_schedules[doctor_id] = node
        return
    cur = head
    while cur["next"] is not None:
        cur = cur["next"]
    cur["next"] = node

def schedule_find_first_free(doctor_schedules, doctor_id):
    head = doctor_schedules.get(doctor_id)
    cur = head
    while cur is not None:
        if cur["slot"]["status"] == "FREE":
            return cur["slot"]
        cur = cur["next"]
    return None

def schedule_find_slot_node(doctor_schedules, slot_id):
    for d_id, head in doctor_schedules.items():
        cur = head
        prev = None
        while cur is not None:
            if cur["slot"]["slot_id"] == slot_id:
                return d_id, prev, cur
            prev = cur
            cur = cur["next"]
    return None, None, None

def schedule_cancel(doctor_schedules, slot_id):
    d_id, prev, node = schedule_find_slot_node(doctor_schedules, slot_id)
    if node is None:
        return False
    if prev is None:
        doctor_schedules[d_id] = node["next"]
    else:
        prev["next"] = node["next"]
    return True

def schedule_next_slot_info(doctor_schedules, doctor_id):
    head = doctor_schedules.get(doctor_id)
    cur = head
    while cur is not None:
        if cur["slot"]["status"] == "FREE":
            s = cur["slot"]
            return f"{s['slot_id']} ({s['start']} - {s['end']})"
        cur = cur["next"]
    return "None"

def count_pending_slots_for_doctor(doctor_schedules, doctor_id):
    head = doctor_schedules.get(doctor_id)
    cur = head
    c = 0
    while cur is not None:
        if cur["slot"]["status"] == "BOOKED":
            c += 1
        cur = cur["next"]
    return c

def patient_upsert(patients, patient):
    patients[patient["id"]] = patient

def patient_get(patients, patient_id):
    return patients.get(patient_id)

def triage_insert(heap, token_id, patient_id, severity):
    heapq.heappush(heap, (severity, token_id, patient_id))

def triage_pop(heap):
    if not heap:
        return None
    return heapq.heappop(heap)

def triage_remove_by_token(heap, token_id):
    new = []
    removed = False
    while heap:
        item = heapq.heappop(heap)
        if item[1] == token_id and not removed:
            removed = True
            continue
        new.append(item)
    for it in new:
        heapq.heappush(heap, it)
    return removed

def undo_push(undo_stack, action):
    undo_stack.append(action)

def undo_pop(undo_stack):
    if not undo_stack:
        return None
    return undo_stack.pop()

def print_doctors(doctors):
    print("\nDoctors:")
    for d_id, d in doctors.items():
        print(f"{d_id}: {d['name']} ({d['specialization']})")

def print_patients(patients):
    print("\nPatients:")
    for p_id, p in patients.items():
        print(f"{p_id}: {p['name']}, Age {p['age']}")

def safe_int(s, default=None):
    try:
        return int(s)
    except:
        return default

def main():
    patients = {}
    doctors = {}
    doctor_schedules = {}
    token_index = {}
    emergency_heap = []
    undo_stack = []
    routine_queue = make_queue(100)
    next_patient_id = 1
    next_token_id = 1
    next_slot_id = 1
    served_count = 0

    doctors[1] = {"id": 1, "name": "Dr. Mehta", "specialization": "Cardiology"}
    doctors[2] = {"id": 2, "name": "Dr. Singh", "specialization": "Orthopedics"}
    doctors[3] = {"id": 3, "name": "Dr. Rao", "specialization": "General Medicine"}

    for d_id in doctors:
        doctor_schedules[d_id] = None

    s1 = make_slot(next_slot_id, "10:00", "10:15", 1)
    next_slot_id += 1
    s2 = make_slot(next_slot_id, "10:15", "10:30", 1)
    next_slot_id += 1
    schedule_add_slot(doctor_schedules, 1, s1)
    schedule_add_slot(doctor_schedules, 1, s2)

    s3 = make_slot(next_slot_id, "11:00", "11:15", 2)
    next_slot_id += 1
    schedule_add_slot(doctor_schedules, 2, s3)

    s4 = make_slot(next_slot_id, "12:00", "12:15", 3)
    next_slot_id += 1
    schedule_add_slot(doctor_schedules, 3, s4)

    while True:
        print("\nHospital Appointment & Triage System")
        print("1. Register Patient")
        print("2. Add Doctor Slot")
        print("3. Book Routine Slot")
        print("4. Emergency In")
        print("5. Serve Next")
        print("6. Undo Last Action")
        print("7. Reports")
        print("8. Show Patients")
        print("9. Show Doctors")
        print("10. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Enter patient name: ").strip()
            age_text = input("Enter age: ").strip()
            if not age_text.isdigit():
                print("Invalid age")
                continue
            age = int(age_text)
            pid = next_patient_id
            next_patient_id += 1
            patient = {"id": pid, "name": name, "age": age, "severity": 0}
            patient_upsert(patients, patient)
            print(f"Registered patient with id {pid}")

        elif choice == "2":
            print_doctors(doctors)
            d_text = input("Enter doctor id: ").strip()
            if not d_text.isdigit() or int(d_text) not in doctors:
                print("Invalid doctor id")
                continue
            d_id = int(d_text)
            start_time = input("Enter start time (e.g., 14:00): ").strip()
            end_time = input("Enter end time (e.g., 14:15): ").strip()
            slot = make_slot(next_slot_id, start_time, end_time, d_id)
            next_slot_id += 1
            schedule_add_slot(doctor_schedules, d_id, slot)
            print(f"Added slot {slot['slot_id']} for doctor {d_id}")

        elif choice == "3":
            if not patients:
                print("No patients registered")
                continue
            print_patients(patients)
            p_text = input("Enter patient id: ").strip()
            if not p_text.isdigit() or int(p_text) not in patients:
                print("Invalid patient id")
                continue
            pid = int(p_text)
            print_doctors(doctors)
            d_text = input("Enter doctor id: ").strip()
            if not d_text.isdigit() or int(d_text) not in doctors:
                print("Invalid doctor id")
                continue
            d_id = int(d_text)
            free_slot = schedule_find_first_free(doctor_schedules, d_id)
            if free_slot is None:
                print("No free slots for this doctor")
                continue
            if queue_is_full(routine_queue):
                print("Routine queue is full")
                continue
            token_id = next_token_id
            next_token_id += 1
            token = {
                "token_id": token_id,
                "patient_id": pid,
                "doctor_id": d_id,
                "slot_id": free_slot["slot_id"],
                "type": "ROUTINE",
            }
            ok = enqueue_routine(routine_queue, token)
            if not ok:
                print("Could not enqueue")
                continue
            free_slot["status"] = "BOOKED"
            token_index[token_id] = token
            action = {
                "kind": "book",
                "mode": "ROUTINE",
                "slot_id": free_slot["slot_id"],
                "token_id": token_id,
            }
            undo_push(undo_stack, action)
            print(f"Booked slot {free_slot['slot_id']} for patient {pid} with token {token_id}")

        elif choice == "4":
            if not patients:
                print("No patients registered")
                continue
            print_patients(patients)
            p_text = input("Enter patient id: ").strip()
            if not p_text.isdigit() or int(p_text) not in patients:
                print("Invalid patient id")
                continue
            pid = int(p_text)
            sev_text = input("Enter severity (lower = more serious): ").strip()
            if not sev_text.isdigit():
                print("Invalid severity")
                continue
            severity = int(sev_text)
            token_id = next_token_id
            next_token_id += 1
            token = {
                "token_id": token_id,
                "patient_id": pid,
                "doctor_id": None,
                "slot_id": None,
                "type": "EMERGENCY",
            }
            token_index[token_id] = token
            triage_insert(emergency_heap, token_id, pid, severity)
            action = {
                "kind": "book",
                "mode": "EMERGENCY",
                "severity": severity,
                "token_id": token_id,
                "patient_id": pid,
            }
            undo_push(undo_stack, action)
            print(f"Emergency patient {pid} added with token {token_id} and severity {severity}")

        elif choice == "5":
            if emergency_heap:
                item = triage_pop(emergency_heap)
                severity, token_id, pid = item
                token_index.pop(token_id, None)
                served_count += 1
                action = {
                    "kind": "serve",
                    "mode": "EMERGENCY",
                    "token_id": token_id,
                    "patient_id": pid,
                    "severity": severity,
                }
                undo_push(undo_stack, action)
                p = patient_get(patients, pid)
                print(f"Serving EMERGENCY patient {pid} ({p['name']}) with token {token_id}, severity {severity}")
            elif not queue_is_empty(routine_queue):
                token = dequeue_routine(routine_queue)
                token_id = token["token_id"]
                pid = token["patient_id"]
                slot_id = token["slot_id"]
                token_index.pop(token_id, None)
                d_id, prev, node = schedule_find_slot_node(doctor_schedules, slot_id)
                old_status = None
                if node is not None:
                    old_status = node["slot"]["status"]
                    node["slot"]["status"] = "SERVED"
                served_count += 1
                action = {
                    "kind": "serve",
                    "mode": "ROUTINE",
                    "token": token,
                    "slot_id": slot_id,
                    "old_status": old_status,
                }
                undo_push(undo_stack, action)
                p = patient_get(patients, pid)
                print(f"Serving routine patient {pid} ({p['name']}) with token {token_id} at slot {slot_id}")
            else:
                print("No patients to serve")

        elif choice == "6":
            action = undo_pop(undo_stack)
            if action is None:
                print("Nothing to undo")
                continue
            if action["kind"] == "book":
                if action["mode"] == "ROUTINE":
                    token_id = action["token_id"]
                    rebuild_queue_excluding(routine_queue, token_id)
                    slot_id = action["slot_id"]
                    d_id, prev, node = schedule_find_slot_node(doctor_schedules, slot_id)
                    if node is not None:
                        node["slot"]["status"] = "FREE"
                    token_index.pop(token_id, None)
                    print(f"Undid routine booking for token {token_id}")
                elif action["mode"] == "EMERGENCY":
                    token_id = action["token_id"]
                    removed = triage_remove_by_token(emergency_heap, token_id)
                    token_index.pop(token_id, None)
                    if removed:
                        print(f"Undid emergency booking for token {token_id}")
                    else:
                        print(f"Emergency token {token_id} not found in heap")
            elif action["kind"] == "serve":
                if action["mode"] == "EMERGENCY":
                    severity = action["severity"]
                    token_id = action["token_id"]
                    pid = action["patient_id"]
                    heapq.heappush(emergency_heap, (severity, token_id, pid))
                    served_count = max(0, served_count - 1)
                    token_index[token_id] = {"token_id": token_id, "patient_id": pid, "doctor_id": None, "slot_id": None, "type": "EMERGENCY"}
                    print(f"Undid serve for emergency token {token_id}")
                elif action["mode"] == "ROUTINE":
                    token = action["token"]
                    slot_id = action["slot_id"]
                    old_status = action["old_status"]
                    ok = rebuild_queue_with_front(routine_queue, token)
                    d_id, prev, node = schedule_find_slot_node(doctor_schedules, slot_id)
                    if node is not None and old_status is not None:
                        node["slot"]["status"] = old_status
                    if ok:
                        served_count = max(0, served_count - 1)
                        token_index[token["token_id"]] = token
                        print(f"Undid serve for routine token {token['token_id']}")
                    else:
                        print("Undo failed, queue full")

        elif choice == "7":
            print("\nReports")
            print("Per doctor pending count and next free slot:")
            for d_id, d in doctors.items():
                pending = count_pending_slots_for_doctor(doctor_schedules, d_id)
                next_slot = schedule_next_slot_info(doctor_schedules, d_id)
                print(f"Doctor {d_id} {d['name']}: Pending={pending}, Next free slot={next_slot}")
            pending_total = routine_queue["count"] + len(emergency_heap)
            print(f"Total served: {served_count}")
            print(f"Total pending (routine + emergency): {pending_total}")

        elif choice == "8":
            if not patients:
                print("No patients")
            else:
                print_patients(patients)

        elif choice == "9":
            print_doctors(doctors)

        elif choice == "10":
            print("Exiting...")
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
